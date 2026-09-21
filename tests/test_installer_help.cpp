#include "installercontroller.h"

#include <QDir>
#include <QFontDatabase>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQmlComponent>
#include <QSignalSpy>
#include <QQuickItem>
#include <QQuickWindow>
#include <QQuickStyle>
#include <QtTest>
#include <algorithm>

class InstallerHelpTest final : public QObject
{
    Q_OBJECT
    static QQuickItem *findVisualItem(QQuickItem *parent, const QString &name)
    {
        if (parent->objectName() == name)
            return parent;
        // Repeater delegates belong to the visual tree, but their QObject
        // ownership does not necessarily descend from the window.
        for (auto *child : parent->childItems()) {
            if (auto *match = findVisualItem(child, name))
                return match;
        }
        return nullptr;
    }

private slots:
    void init()
    {
        // Rendering warnings must fail normal UI acceptance, including native
        // SVG/image diagnostics that are not QQmlEngine::warnings signals.
        QTest::failOnWarning(QRegularExpression(QStringLiteral(".*")));
    }

    void initTestCase()
    {
        QQuickStyle::setStyle(QStringLiteral("Basic"));
        QFontDatabase::addApplicationFont(QStringLiteral(":/assets/fonts/AdwaitaSans-Regular.ttf"));
        QGuiApplication::setFont(QFont(QStringLiteral("Adwaita Sans"), 10));
    }

    void everyScreenLoadsWithoutContextGlobals_data()
    {
        QTest::addColumn<bool>("oobe");
        QTest::addColumn<bool>("documentation");
        QTest::addColumn<int>("width");
        for (bool oobe : {false, true}) {
            for (bool documentation : {false, true}) {
                for (int width : {1024, 1920}) {
                    QTest::newRow(qPrintable(QStringLiteral("%1-doc%2-%3")
                        .arg(oobe ? "oobe" : "install").arg(documentation).arg(width)))
                        << oobe << documentation << width;
                }
            }
        }
    }

    void everyScreenLoadsWithoutContextGlobals()
    {
        QFETCH(bool, oobe);
        QFETCH(bool, documentation);
        QFETCH(int, width);
        InstallerController controller(oobe, true, "/unused/backend");
        QQmlApplicationEngine engine;
        engine.setOutputWarningsToStandardError(false);
        QSignalSpy warnings(&engine, &QQmlEngine::warnings);
        QVERIFY(!engine.rootContext()->contextProperty("controller").isValid());
        engine.setInitialProperties({
            {"controller", QVariant::fromValue(&controller)}, {"captureMode", true},
            {"documentationMode", documentation}, {"captureWidth", width},
            {"captureHeight", width == 1920 ? 1080 : 768}});
        engine.load(QUrl("qrc:/qml/Main.qml"));
        QVERIFY(!engine.rootObjects().isEmpty());
        auto *window = qobject_cast<QQuickWindow *>(engine.rootObjects().constFirst());
        QVERIFY(window);
        QVERIFY(QTest::qWaitForWindowExposed(window));
        QCOMPARE(window->width(), width);
        QCOMPARE(window->height(), width == 1920 ? 1080 : 768);
        auto *loader = window->findChild<QObject *>("setupScreenLoader");
        QVERIFY(loader);
        auto checkLoaded = [&](const QString &screen) {
            QCOMPARE(loader->property("status").toInt(), 1); // Loader.Ready
            QCOMPARE(loader->property("source").toUrl(), QUrl("qrc:/qml/screens/" + screen + ".qml"));
            auto *item = qvariant_cast<QObject *>(loader->property("item"));
            QVERIFY(item);
            QCOMPARE(qvariant_cast<QObject *>(item->property("controller")), &controller);
            QCOMPARE(item->property("documentationMode").toBool(), documentation);
        };
        checkLoaded(controller.screenId());
        FlowState flow(oobe ? FlowState::Mode::Oobe : FlowState::Mode::Installer);
        QStringList screens;
        do {
            screens.append(flow.screenId());
        } while (flow.next());
        // Reuse the SAME engine in both directions: this catches Loader input
        // regressions after initial construction, not merely isolated pages.
        for (int pass = 0; pass < 2; ++pass) {
            for (const auto &screen : screens) {
                QVERIFY(controller.jumpToForTest(screen));
                QTest::qWait(50); // Includes repaint-guard release and a render.
                QCOMPARE(controller.screenId(), screen);
                checkLoaded(screen);
                const auto capture = qEnvironmentVariable("AERO7_QA_SCREENSHOT_DIR");
                if (!capture.isEmpty() && documentation && width == 1920 && pass == 0) {
                    QVERIFY(QDir().mkpath(capture));
                    QVERIFY(window->grabWindow().save(capture + "/explicit-" + screen + ".png"));
                }
            }
            std::reverse(screens.begin(), screens.end());
        }
        for (const auto &arguments : warnings) {
            for (const auto &warning : qvariant_cast<QList<QQmlError>>(arguments.constFirst()))
                qWarning().noquote() << warning.toString();
        }
        QCOMPARE(warnings.size(), 0);
    }

    void missingControllerIsRejected()
    {
        QQmlEngine engine;
        // Failed creations intentionally evaluate bindings without their input.
        // Assert the component errors below; keep this negative test's expected
        // diagnostics separate from the warning-free normal loading test.
        engine.setOutputWarningsToStandardError(false);
        QStringList paths {QStringLiteral("qrc:/qml/Main.qml")};
        for (const auto &name : QDir(":/qml/screens").entryList({"*.qml"}, QDir::Files))
            paths.append("qrc:/qml/screens/" + name);
        QCOMPARE(paths.size(), 21);
        for (const auto &path : paths) {
            QQmlComponent component(&engine, QUrl(path));
            QVERIFY2(component.isReady(), qPrintable(component.errorString()));
            QScopedPointer<QObject> object(component.create());
            QVERIFY2(!object, qPrintable(path + " accepted a missing controller"));
            QVERIFY2(component.errorString().contains("Required property controller was not initialized"),
                qPrintable(component.errorString()));
        }
    }

    void approvedIconsRenderWhenVisible()
    {
        for (bool oobe : {false, true}) {
            InstallerController controller(oobe, true, "/unused/backend");
            if (!oobe)
                controller.selectDisk(0);
            QVERIFY(controller.jumpToForTest(oobe ? "DesktopScreen" : "ConfirmScreen"));
            QQmlApplicationEngine engine;
            engine.setInitialProperties({
                {"controller", QVariant::fromValue(&controller)}, {"captureMode", true},
                {"documentationMode", true}, {"captureWidth", 1920}, {"captureHeight", 1080}});
            engine.load(QUrl("qrc:/qml/Main.qml"));
            QVERIFY(!engine.rootObjects().isEmpty());
            auto *window = qobject_cast<QQuickWindow *>(engine.rootObjects().constFirst());
            QVERIFY(window);
            QVERIFY(QTest::qWaitForWindowExposed(window));
            if (!oobe) {
                controller.goNext(); // Actual simulated progress updates, no injected stage.
                QTRY_VERIFY_WITH_TIMEOUT(controller.progressStageIndex() >= 2, 10000);
            }
            auto *icon = findVisualItem(window->contentItem(), oobe
                ? "setupRecycleBinIcon" : "setupCompletedStageIcon0");
            QVERIFY(icon);
            QTRY_VERIFY(icon->isVisible());
            QCOMPARE(icon->property("status").toInt(), 1); // Image.Ready
            QCOMPARE(icon->property("source").toUrl(), QUrl(oobe
                ? "qrc:/assets/icons/recycle-bin.png" : "qrc:/assets/icons/check-green.png"));
            const auto capture = qEnvironmentVariable("AERO7_QA_SCREENSHOT_DIR");
            if (!capture.isEmpty()) {
                QVERIFY(QDir().mkpath(capture));
                QTest::qWait(150);
                QVERIFY(window->grabWindow().save(capture + (oobe
                    ? "/approved-recycle-bin-1920.png" : "/approved-progress-check-1920.png")));
            }
        }
    }

    void backAndNextUseInjectedController()
    {
        InstallerController controller(false, true, "/unused/backend");
        QQmlApplicationEngine engine;
        QSignalSpy warnings(&engine, &QQmlEngine::warnings);
        engine.setInitialProperties({
            {"controller", QVariant::fromValue(&controller)}, {"captureMode", true}});
        engine.load(QUrl("qrc:/qml/Main.qml"));
        QVERIFY(!engine.rootObjects().isEmpty());
        auto *window = qobject_cast<QQuickWindow *>(engine.rootObjects().constFirst());
        QVERIFY(window);
        QVERIFY(QTest::qWaitForWindowExposed(window));
        auto click = [&](const QString &name) {
            auto *button = window->findChild<QQuickItem *>(name);
            QVERIFY(button);
            QVERIFY(button->isVisible());
            QVERIFY(button->isEnabled());
            QTest::mouseClick(window, Qt::LeftButton, Qt::NoModifier,
                button->mapToScene(QPointF(button->width() / 2, button->height() / 2)).toPoint());
        };
        QVERIFY(controller.jumpToForTest("WelcomeScreen"));
        QTest::qWait(50);
        click("setupBackButton");
        QCOMPARE(controller.screenId(), QStringLiteral("LanguageScreen"));
        QVERIFY(controller.jumpToForTest("DiskScreen"));
        controller.selectDisk(0);
        QVERIFY(controller.diskSelectionReady());
        QTest::qWait(50);
        click("setupNextButton");
        QCOMPARE(controller.screenId(), QStringLiteral("ConfirmScreen"));
        QTest::qWait(50);
        click("setupBackButton");
        QCOMPARE(controller.screenId(), QStringLiteral("DiskScreen"));
        QCOMPARE(warnings.size(), 0);
    }

    void opensWithoutAdvancingSetup_data()
    {
        QTest::addColumn<QString>("screen");
        QTest::addColumn<QString>("linkName");
        QTest::addColumn<QString>("dialogName");
        QTest::addColumn<int>("width");
        for (const int width : {1024, 1920}) {
            QTest::newRow(qPrintable(QStringLiteral("updates-%1").arg(width)))
                << QStringLiteral("UpdatesScreen") << QStringLiteral("updateOptionsHelp") << QStringLiteral("updateOptionsDialog") << width;
            QTest::newRow(qPrintable(QStringLiteral("privacy-%1").arg(width)))
                << QStringLiteral("UpdatesScreen") << QStringLiteral("setupPrivacyHelp") << QStringLiteral("setupPrivacyDialog") << width;
            QTest::newRow(qPrintable(QStringLiteral("install-type-%1").arg(width)))
                << QStringLiteral("InstallTypeScreen") << QStringLiteral("installTypeHelp") << QStringLiteral("installTypeDialog") << width;
        }
    }

    void timePreviewReactsToZoneChange()
    {
        InstallerController controller(true, true, "/unused/backend");
        QVERIFY(controller.jumpToForTest("TimeScreen"));
        QQmlApplicationEngine engine;
        engine.setInitialProperties({
            {"controller", QVariant::fromValue(&controller)}, {"captureMode", true},
            {"documentationMode", false}, {"captureWidth", 1920}, {"captureHeight", 1080}});
        engine.load(QUrl("qrc:/qml/Main.qml"));
        QVERIFY(!engine.rootObjects().isEmpty());
        auto *window = qobject_cast<QQuickWindow *>(engine.rootObjects().constFirst());
        QVERIFY(window);
        QVERIFY(QTest::qWaitForWindowExposed(window));
        QObject *clock = nullptr;
        QTRY_VERIFY((clock = window->findChild<QObject *>("setupTimeClock")) != nullptr);
        auto *text = window->findChild<QObject *>("setupTimeText");
        QVERIFY(text);
        for (const QString &zone : {QStringLiteral("Europe/Amsterdam"), QStringLiteral("Asia/Tokyo")}) {
            controller.setProperty("timezone", zone);
            const auto preview = controller.clockPreview(QDateTime::currentMSecsSinceEpoch(), zone);
            QTRY_COMPARE(clock->property("hours").toInt(), preview.value("hour").toInt());
            QTRY_VERIFY(text->property("text").toString().endsWith(preview.value("abbreviation").toString()));
        }
        QCOMPARE(controller.screenId(), QStringLiteral("TimeScreen"));
        const auto capture = qEnvironmentVariable("AERO7_QA_SCREENSHOT_DIR");
        if (!capture.isEmpty()) {
            QVERIFY(QDir().mkpath(capture));
            QTest::qWait(150);
            QVERIFY(window->grabWindow().save(capture + "/time-preview-tokyo-1920.png"));
        }
        controller.setProperty("timezone", "Europe/Amsterdam");
        for (const QString &region : {QStringLiteral("Nederlands (Nederland)"), QStringLiteral("English (United States)")}) {
            controller.setProperty("timeFormat", region);
            const bool dutch = region.startsWith("Nederlands");
            // The timer must refresh the QML binding after the format changes.
            QTRY_VERIFY_WITH_TIMEOUT(text->property("text").toString().contains("AM")
                || text->property("text").toString().contains("PM")
                ? !dutch : dutch, 3000);
            if (!capture.isEmpty()) {
                QTest::qWait(150);
                QVERIFY(window->grabWindow().save(capture + (dutch
                    ? "/time-preview-dutch-1920.png" : "/time-preview-us-1920.png")));
            }
        }
    }

    void opensWithoutAdvancingSetup()
    {
        QFETCH(QString, screen);
        QFETCH(QString, linkName);
        QFETCH(QString, dialogName);
        QFETCH(int, width);
        InstallerController controller(screen == "UpdatesScreen", true, "/unused/backend");
        QVERIFY(controller.jumpToForTest(screen));
        const auto preference = controller.property("updatePreference");
        QQmlApplicationEngine engine;
        engine.setInitialProperties({
            {"controller", QVariant::fromValue(&controller)}, {"captureMode", true},
            {"documentationMode", false}, {"captureWidth", width},
            {"captureHeight", width == 1920 ? 1080 : 768}});
        engine.load(QUrl("qrc:/qml/Main.qml"));
        QVERIFY(!engine.rootObjects().isEmpty());
        auto *window = qobject_cast<QQuickWindow *>(engine.rootObjects().constFirst());
        QVERIFY(window);
        QVERIFY(QTest::qWaitForWindowExposed(window));
        QQuickItem *link = nullptr;
        QTRY_VERIFY((link = window->findChild<QQuickItem *>(linkName)) != nullptr);
        auto *dialog = window->findChild<QObject *>(dialogName);
        QVERIFY(dialog);
        QVERIFY(link->isVisible());
        QTest::mouseClick(window, Qt::LeftButton, Qt::NoModifier,
            link->mapToScene(QPointF(link->width() / 2, link->height() / 2)).toPoint());
        QTRY_VERIFY(dialog->property("opened").toBool());
        QVERIFY(dialog->property("modal").toBool());
        QVERIFY(dialog->property("message").toString().size() > 100);
        QVERIFY(dialog->property("height").toReal() < window->height());
        QCOMPARE(controller.screenId(), screen);
        QCOMPARE(controller.property("updatePreference"), preference);

        const auto capture = qEnvironmentVariable("AERO7_QA_SCREENSHOT_DIR");
        if (!capture.isEmpty()) {
            QVERIFY(QDir().mkpath(capture));
            QTest::qWait(150);
            QVERIFY(window->grabWindow().save(capture + "/" + dialogName + "-" + QString::number(width) + ".png"));
        }
        QTest::keyClick(window, Qt::Key_Escape);
        QTRY_VERIFY(!dialog->property("visible").toBool());
        link->forceActiveFocus();
        QTest::keyClick(window, Qt::Key_Space);
        QTRY_VERIFY(dialog->property("opened").toBool());
        auto *close = dialog->findChild<QQuickItem *>("setupHelpClose");
        QVERIFY(close);
        QTRY_VERIFY(close->hasActiveFocus());
        QTest::keyClick(window, Qt::Key_Space);
        QTRY_VERIFY(!dialog->property("visible").toBool());
        QCOMPARE(controller.screenId(), screen);
    }
};

QTEST_MAIN(InstallerHelpTest)
#include "test_installer_help.moc"
