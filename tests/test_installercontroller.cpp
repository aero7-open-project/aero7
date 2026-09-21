#include "installercontroller.h"

#include <QtTest>

class InstallerControllerTest final : public QObject
{
    Q_OBJECT

private slots:
    void clockPreviewUsesSelectedRegionalFormat()
    {
        InstallerController controller(true, true, QStringLiteral("/unused/backend"));
        const auto instant = QDateTime::fromString(QStringLiteral("2026-01-06T17:49:06Z"), Qt::ISODate).toMSecsSinceEpoch();
        for (const auto &choice : {qMakePair(QStringLiteral("Nederlands (Nederland)"), QLocale("nl_NL")),
                                   qMakePair(QStringLiteral("English (United States)"), QLocale("en_US"))}) {
            controller.setProperty("timeFormat", choice.first);
            const auto preview = controller.clockPreview(instant, "Europe/Amsterdam");
            QCOMPARE(preview.value("hour").toInt(), 18);
            QCOMPARE(preview.value("timeText").toString().simplified(), choice.second.language() == QLocale::Dutch
                ? QStringLiteral("18:49:06") : QStringLiteral("6:49:06 PM"));
            QCOMPARE(preview.value("monthTitle").toString(), choice.second.toString(QDate(2026, 1, 6), "MMMM yyyy"));
            QCOMPARE(preview.value("firstWeekday").toInt(), choice.second.language() == QLocale::Dutch ? 3 : 4);
            const auto names = preview.value("weekdayNames").toStringList();
            QCOMPARE(names.size(), 7);
            QCOMPARE(names.first(), choice.second.standaloneDayName(choice.second.firstDayOfWeek(), QLocale::ShortFormat));
        }
    }

    void clockPreviewUsesSelectedZoneAndDaylightRules()
    {
        InstallerController controller(true, true, QStringLiteral("/unused/backend"));
        const auto epoch = [](const char *iso) {
            return QDateTime::fromString(QString::fromLatin1(iso), Qt::ISODate).toMSecsSinceEpoch();
        };
        const auto summer = controller.clockPreview(epoch("2026-09-06T15:19:52Z"), "Europe/Amsterdam");
        QVERIFY(summer.value("valid").toBool());
        QCOMPARE(summer.value("hour").toInt(), 17);
        QCOMPARE(summer.value("minute").toInt(), 19);
        QCOMPARE(summer.value("second").toInt(), 52);
        QCOMPARE(summer.value("offsetSeconds").toInt(), 7200);
        const auto winter = controller.clockPreview(epoch("2026-01-06T15:19:52Z"), "Europe/Amsterdam");
        QCOMPARE(winter.value("hour").toInt(), 16);
        QCOMPARE(winter.value("offsetSeconds").toInt(), 3600);
        const auto beforeDst = controller.clockPreview(epoch("2026-03-29T00:59:59Z"), "Europe/Amsterdam");
        const auto afterDst = controller.clockPreview(epoch("2026-03-29T01:00:00Z"), "Europe/Amsterdam");
        QCOMPARE(beforeDst.value("hour").toInt(), 1);
        QCOMPARE(afterDst.value("hour").toInt(), 3);
        const auto tokyo = controller.clockPreview(epoch("2026-12-31T20:00:00Z"), "Asia/Tokyo");
        QCOMPARE(tokyo.value("year").toInt(), 2027);
        QCOMPARE(tokyo.value("month").toInt(), 1);
        QCOMPARE(tokyo.value("day").toInt(), 1);
        QCOMPARE(tokyo.value("hour").toInt(), 5);
        QCOMPARE(tokyo.value("firstWeekday").toInt(), 5);
        QCOMPARE(tokyo.value("daysInMonth").toInt(), 31);
        QVERIFY(!controller.clockPreview(epoch("2026-09-06T15:19:52Z"), "Not/AZone").value("valid").toBool());
    }

    void serializesIndependentInstallationPreferences()
    {
        InstallerController controller(false, true, QStringLiteral("/unused/backend"));
        QCOMPARE(controller.installationPreferences().value("keyboard").toString(), QStringLiteral("US"));
        controller.setProperty("language", QStringLiteral("Nederlands"));
        controller.setProperty("timeFormat", QStringLiteral("English (United States)"));
        controller.setProperty("keyboard", QStringLiteral("Dutch"));
        const auto settings = controller.installationPreferences();
        QCOMPARE(settings.size(), 3);
        QCOMPARE(settings.value("language").toString(), QStringLiteral("Nederlands"));
        QCOMPARE(settings.value("time_format").toString(), QStringLiteral("English (United States)"));
        QCOMPARE(settings.value("keyboard").toString(), QStringLiteral("Dutch"));
    }

    void completesFullSimulationFlow()
    {
        InstallerController controller(false, true, QStringLiteral("/unused/backend"));

        QCOMPARE(controller.screenId(), QStringLiteral("LanguageScreen"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("WelcomeScreen"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("StartingScreen"));
        QTRY_COMPARE_WITH_TIMEOUT(controller.screenId(), QStringLiteral("LicenseScreen"), 3000);

        controller.setProperty("licenseAccepted", true);
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("InstallTypeScreen"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("DiskScreen"));
        controller.selectDisk(0);
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("ConfirmScreen"));

        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("ProgressScreen"));
        QCOMPARE(controller.progressStagePercent(), 0);
        QTRY_VERIFY_WITH_TIMEOUT(controller.progressStagePercent() > 0, 1000);
        QTRY_COMPARE_WITH_TIMEOUT(controller.screenId(), QStringLiteral("CompleteScreen"), 8000);
        QCOMPARE(controller.progressStagePercent(), 100);
        QCOMPARE(controller.restartSeconds(), 10);

        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("ApplyingSettingsScreen"));
        QVERIFY(controller.oobeMode());
        QTRY_COMPARE_WITH_TIMEOUT(controller.screenId(), QStringLiteral("VideoPerformanceScreen"), 3500);
        QTRY_COMPARE_WITH_TIMEOUT(controller.screenId(), QStringLiteral("AccountScreen"), 4000);

        controller.setProperty("username", QStringLiteral("geko"));
        controller.setProperty("computerName", QStringLiteral("aero7-pc"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("PasswordScreen"));
        controller.setProperty("password", QStringLiteral("correct-horse"));
        controller.setProperty("passwordConfirmation", QStringLiteral("correct-horse"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("UpdatesScreen"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("TimeScreen"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("NetworkScreen"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("FinalizingScreen"));

        QTRY_COMPARE_WITH_TIMEOUT(controller.screenId(), QStringLiteral("OobeWelcomeScreen"), 8000);
        QTRY_COMPARE_WITH_TIMEOUT(controller.screenId(), QStringLiteral("PreparingDesktopScreen"), 3500);
        QTRY_COMPARE_WITH_TIMEOUT(controller.screenId(), QStringLiteral("DesktopScreen"), 4000);
        QCOMPARE(controller.progress(), 100);

        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("LanguageScreen"));
        QVERIFY(!controller.oobeMode());
    }

    void rejectsInvalidAccountAndPassword()
    {
        InstallerController controller(true, true, QStringLiteral("/unused/backend"));
        QVERIFY(controller.jumpToForTest(QStringLiteral("AccountScreen")));
        controller.setProperty("username", QStringLiteral("Upper Case"));
        controller.setProperty("computerName", QStringLiteral("-invalid"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("AccountScreen"));
        QVERIFY(!controller.statusText().isEmpty());

        controller.setProperty("username", QStringLiteral("valid_user"));
        controller.setProperty("computerName", QStringLiteral("aero7-pc"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("PasswordScreen"));
        controller.setProperty("password", QStringLiteral("bad:password"));
        controller.setProperty("passwordConfirmation", QStringLiteral("bad:password"));
        controller.goNext();
        QCOMPARE(controller.screenId(), QStringLiteral("PasswordScreen"));
        QVERIFY(controller.statusText().contains(QLatin1Char(':')));
    }

    void recoveryShellIsSafeInSimulation()
    {
        InstallerController controller(false, true, QStringLiteral("/unused/backend"));
        controller.openRecoveryShell();
        QVERIFY(controller.statusText().contains(QStringLiteral("TTY2")));
        QCOMPARE(controller.screenId(), QStringLiteral("LanguageScreen"));
    }

    void preparesAdvancedPartitionTargetsInSimulation()
    {
        InstallerController controller(false, true, QStringLiteral("/unused/backend"));
        QCOMPARE(controller.disks().size(), 4);
        QVERIFY(controller.diskSelectionReady());

        controller.setAdvancedDriveOptions(true);
        QVERIFY(controller.advancedDriveOptions());
        QVERIFY(controller.selectedDisk().isEmpty());
        QVERIFY(!controller.diskSelectionReady());

        controller.selectDisk(1);
        QCOMPARE(controller.selectedDisk().value(QStringLiteral("type")).toString(),
                 QStringLiteral("System"));
        QVERIFY(!controller.diskSelectionReady());

        controller.selectDisk(2);
        QVERIFY(!controller.diskSelectionReady());
        controller.prepareSelectedNtfsShrink(17);
        QCOMPARE(
            controller.selectedDisk().value(QStringLiteral("target_kind")).toString(),
            QStringLiteral("shrink_ntfs"));
        QVERIFY(controller.diskSelectionReady());

        controller.selectDisk(3);
        QCOMPARE(
            controller.selectedDisk().value(QStringLiteral("target_kind")).toString(),
            QStringLiteral("free"));
        QVERIFY(!controller.diskSelectionReady());
        controller.useSelectedFreeSpace(24);
        QVERIFY(controller.diskSelectionReady());
        QVERIFY(controller.statusText().contains(QStringLiteral("1 GiB")));

        controller.selectDisk(2);
        controller.useSelectedPartition();
        QCOMPARE(
            controller.selectedDisk().value(QStringLiteral("target_kind")).toString(),
            QStringLiteral("reuse_partition"));
        QVERIFY(controller.diskSelectionReady());

        controller.setAdvancedDriveOptions(false);
        QVERIFY(controller.selectedDisk().isEmpty());
        QVERIFY(!controller.diskSelectionReady());
    }

    void simulatesDeleteAndExtendActions()
    {
        InstallerController controller(false, true, QStringLiteral("/unused/backend"));
        controller.setAdvancedDriveOptions(true);
        controller.selectDisk(2);
        QVERIFY(controller.selectedDisk().value(QStringLiteral("can_delete")).toBool());
        QVERIFY(controller.selectedDisk().value(QStringLiteral("can_extend")).toBool());

        controller.extendSelectedPartition(2);
        QVERIFY(controller.statusText().contains(QStringLiteral("extended")));
        QCOMPARE(controller.selectedDisk().value(QStringLiteral("size")).toString(),
                 QStringLiteral("47 GiB"));

        controller.selectDisk(2);
        controller.deleteSelectedPartition();
        QCOMPARE(controller.selectedDisk().value(QStringLiteral("target_kind")).toString(),
                 QStringLiteral("free"));
        QVERIFY(controller.statusText().contains(QStringLiteral("unallocated")));
        QVERIFY(!controller.diskSelectionReady());
    }

    void exposesBackendFailureOnProgressScreen()
    {
        InstallerController controller(false, true, QStringLiteral("/unused/backend"));
        QVERIFY(controller.jumpToForTest(QStringLiteral("ProgressScreen")));

        QVERIFY(QMetaObject::invokeMethod(
            &controller, "backendFinished", Qt::DirectConnection,
            Q_ARG(int, 2), Q_ARG(QProcess::ExitStatus, QProcess::NormalExit)));

        QVERIFY(controller.setupFailed());
        QVERIFY(controller.failureDetails().contains(QStringLiteral("code 2")));
        QCOMPARE(controller.progressStage(), QStringLiteral("Installation stopped"));
        QVERIFY(controller.statusText().startsWith(QStringLiteral("Setup stopped safely.")));
        QVERIFY(!controller.busy());
        QCOMPARE(controller.screenId(), QStringLiteral("ProgressScreen"));
    }
};

QTEST_GUILESS_MAIN(InstallerControllerTest)
#include "test_installercontroller.moc"
