#include <QtTest>
#include <QCoreApplication>
#include "../imagius/src/imagius_utils.h"

// add necessary includes here

class Test_Imagius_Utils : public QObject
{
        Q_OBJECT

    private slots:
        void UserAppDataDir();

};

//Test_Imagius_Utils::Test_Imagius_Utils()
//{

//}

//Test_Imagius_Utils::~Test_Imagius_Utils()
//{

//}

void Test_Imagius_Utils::UserAppDataDir() {

    qDebug() << Imagius_Utils::UserAppDataDir();
    QCOMPARE(Imagius_Utils::UserAppDataDir(), QString("C:/Users/Julien/AppData/Roaming/tests"));
}

QTEST_MAIN(Test_Imagius_Utils)

#include "tst_test_imagius_utils.moc"
