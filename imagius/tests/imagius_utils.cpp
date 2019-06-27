#include <QtTest/QtTest>
#include <src/imagius_utils.h>

class Test_Imagius_Utils: public QObject {
    Q_OBJECT
private slots:
    void UserAppDataDir();
};

void Test_Imagius_Utils::UserAppDataDir() {
    QCOMPARE(Imagius_Utils::UserAppDataDir(), QString("test"));
}

QTEST_MAIN(Test_Imagius_Utils)
#include "test_imagius_utils.moc"
