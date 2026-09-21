// SPDX-License-Identifier: GPL-2.0-or-later
// Execute extracted KWin session methods with controlled protocol collaborators.
// This tests control flow, not real Wayland, D-Bus, notification transport or ABI.
#include <QtTest>
#include <QDBusError>
#include <QLoggingCategory>
#include <QPointer>
#include <algorithm>
#include <chrono>
#include <memory>

using namespace Qt::StringLiterals;
Q_LOGGING_CATEGORY(KWIN_CORE, "aero7.test.logout")

class ControlledTimer : public QObject
{
    Q_OBJECT
public:
    inline static QList<ControlledTimer *> timers;
    inline static qint64 now = 0;
    bool active = false;
    bool singleShot = false;
    qint64 deadline = 0;
    ControlledTimer() { timers.append(this); }
    ~ControlledTimer() override { timers.removeOne(this); }
    template<typename Rep, typename Period>
    void start(std::chrono::duration<Rep, Period> duration)
    {
        deadline = now + std::chrono::duration_cast<std::chrono::milliseconds>(duration).count();
        active = true;
    }
    void stop() { active = false; }
    void setSingleShot(bool value) { singleShot = value; }
    static void advance(qint64 milliseconds)
    {
        const auto end = now + milliseconds;
        while (true) {
            ControlledTimer *next = nullptr;
            for (auto timer : std::as_const(timers)) {
                if (timer->active && timer->deadline <= end && (!next || timer->deadline < next->deadline)) {
                    next = timer;
                }
            }
            if (!next) break;
            now = next->deadline;
            next->active = false;
            Q_EMIT next->timeout();
        }
        now = end;
    }
Q_SIGNALS:
    void timeout();
};

class XdgToplevelWindow : public QObject
{
    Q_OBJECT
public:
    int closeRequests = 0;
    void closeWindow() { ++closeRequests; }
    QString desktopFileName() const { return u"qa-editor"_s; }
    QString caption() const { return u"Unsaved QA document"_s; }
Q_SIGNALS:
    void closed();
};

class KNotificationAction : public QObject
{
    Q_OBJECT
public:
    using QObject::QObject;
Q_SIGNALS:
    void activated();
};

class KNotification : public QObject
{
    Q_OBJECT
public:
    enum { DefaultEvent = 1, Persistent = 2 };
    QList<KNotificationAction *> actions;
    QString text;
    KNotification(const char *, int) {}
    void setText(const QString &value) { text = value; }
    KNotificationAction *addAction(const QString &)
    {
        auto action = new KNotificationAction(this);
        actions.append(action);
        return action;
    }
    void sendEvent() {}
    void close() { Q_EMIT closed(); }
Q_SIGNALS:
    void closed();
};

struct KService {
    static std::shared_ptr<KService> serviceByDesktopName(const QString &) { return {}; }
    QString name() const { return u"QA editor"_s; }
};
QString i18nc(const char *, const char *text) { return QString::fromUtf8(text); }
QString i18n(const char *text, const QString &argument) { return QString::fromUtf8(text).arg(argument); }

struct Message { bool createReply(bool success) const { return success; } };
struct Connection {
    inline static QList<bool> replies;
    static Connection sessionBus() { return {}; }
    void send(bool success) { replies.append(success); }
};
struct Workspace {
    QList<QObject *> clients;
    QList<QObject *> windows() const { return clients; }
};
Workspace testWorkspace;
Workspace *workspace() { return &testWorkspace; }

#define QTimer ControlledTimer
#define QDBusConnection Connection
#ifndef KWIN_BUILD_NOTIFICATIONS
#define KWIN_BUILD_NOTIFICATIONS 1
#endif
class SessionManager : public QObject
{
public:
    QList<XdgToplevelWindow *> m_pendingWindows;
    QTimer m_closeTimer;
    QTimer m_logoutAnywayTimer; // Also supports the unpatched negative fixture.
    std::unique_ptr<QObject> m_closingWindowsGuard;
    QPointer<KNotification> m_cancelNotification;
    int rejectedRequests = 0;
    bool calledFromDBus() const { return true; }
    Message message() const { return {}; }
    void setDelayedReply(bool) {}
    void sendErrorReply(QDBusError::ErrorType, const QString &) { ++rejectedRequests; }
    bool closeWaylandWindows();
    void updateWaylandCancelNotification();
    ~SessionManager() override
    {
        m_closingWindowsGuard.reset();
        delete m_cancelNotification;
    }
};
#include "production-session-methods.inc"
#undef QTimer
#undef QDBusConnection

class LogoutTest : public QObject
{
    Q_OBJECT
private Q_SLOTS:
    void init()
    {
        Connection::replies.clear();
        testWorkspace.clients.clear();
        ControlledTimer::now = 0;
    }
#if KWIN_BUILD_NOTIFICATIONS
    void pendingWindowSurvivesFormerForceDeadline()
    {
        XdgToplevelWindow window;
        testWorkspace.clients = {&window};
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        QCOMPARE(window.closeRequests, 1);
        ControlledTimer::advance(180000);
        QVERIFY2(Connection::replies.isEmpty(), "Elapsed time authorized abandonment of a pending window");
        QVERIFY(session.m_closingWindowsGuard);
        QVERIFY(session.m_cancelNotification);
        QVERIFY(session.m_cancelNotification->text.contains("may discard unsaved work"));
    }
    void cancelRejectsLogoutAndDisconnectsLaterTimers()
    {
        XdgToplevelWindow window;
        testWorkspace.clients = {&window};
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        ControlledTimer::advance(10000);
        session.m_cancelNotification->actions.at(0)->activated();
        ControlledTimer::advance(180000);
        QCOMPARE(Connection::replies, QList<bool>{false});
        QVERIFY(!session.m_closingWindowsGuard);
    }
    void explicitOverrideAllowsLogoutExactlyOnce()
    {
        XdgToplevelWindow window;
        testWorkspace.clients = {&window};
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        ControlledTimer::advance(10000);
        session.m_cancelNotification->actions.at(1)->activated();
        session.m_cancelNotification->close();
        ControlledTimer::advance(180000);
        QCOMPARE(Connection::replies, QList<bool>{true});
    }
    void notificationDismissalRejectsLogout()
    {
        XdgToplevelWindow window;
        testWorkspace.clients = {&window};
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        ControlledTimer::advance(10000);
        session.m_cancelNotification->close();
        ControlledTimer::advance(180000);
        QCOMPARE(Connection::replies, QList<bool>{false});
    }
#endif
    void allWindowsClosingBeforeNoticeCompletesNormally()
    {
        XdgToplevelWindow first, second;
        testWorkspace.clients = {&first, &second};
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        first.closed();
        QVERIFY(Connection::replies.isEmpty());
        second.closed();
        ControlledTimer::advance(180000);
        QCOMPARE(Connection::replies, QList<bool>{true});
    }
    void noWindowsCompletesImmediately()
    {
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        QCOMPARE(Connection::replies, QList<bool>{true});
    }
#if KWIN_BUILD_NOTIFICATIONS
    void allWindowsClosingAfterNoticeCompletesExactlyOnce()
    {
        XdgToplevelWindow window;
        testWorkspace.clients = {&window};
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        ControlledTimer::advance(10000);
        QVERIFY(session.m_cancelNotification);
        // Closing a notification may emit closed() synchronously. Programmatic
        // cleanup must not turn successful window closure into cancellation.
        window.closed();
        QCOMPARE(Connection::replies, QList<bool>{true});
    }
    void cancelledOperationCanBeRetried()
    {
        XdgToplevelWindow window;
        testWorkspace.clients = {&window};
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        ControlledTimer::advance(10000);
        session.m_cancelNotification->actions.at(0)->activated();
        delete session.m_cancelNotification;
        QVERIFY(session.closeWaylandWindows());
        QCOMPARE(window.closeRequests, 2);
        ControlledTimer::advance(10000);
        session.m_cancelNotification->actions.at(1)->activated();
        ControlledTimer::advance(180000);
        QCOMPARE(Connection::replies, (QList<bool>{false, true}));
    }
#else
    void unavailableNotificationSupportCancelsSafely()
    {
        XdgToplevelWindow window;
        testWorkspace.clients = {&window};
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        ControlledTimer::advance(180000);
        QCOMPARE(Connection::replies, QList<bool>{false});
        QVERIFY(!session.m_closingWindowsGuard);
        QVERIFY(!session.m_cancelNotification);
        QVERIFY(session.closeWaylandWindows());
        ControlledTimer::advance(180000);
        QCOMPARE(Connection::replies, (QList<bool>{false, false}));
    }
#endif
    void concurrentRequestDoesNotReplacePendingOperation()
    {
        XdgToplevelWindow window;
        testWorkspace.clients = {&window};
        SessionManager session;
        QVERIFY(session.closeWaylandWindows());
        QVERIFY(!session.closeWaylandWindows());
        QCOMPARE(session.rejectedRequests, 1);
        QCOMPARE(window.closeRequests, 1);
        QVERIFY(Connection::replies.isEmpty());
    }
};
QTEST_GUILESS_MAIN(LogoutTest)
#include "kwin_logout_harness.moc"
