

#include <OTMql4/OTLibLog.mqh>
#include <OTMql4/OTLibPy27.mqh>

#include <WinUser32.mqh>

extern string sStdOutFile="_test_OTMql4PyTest.txt";

extern bool bTestStdout=true;
extern bool bTestDatatypes=true;
extern bool bTestImport=true;
extern bool bTestMessageBox=true;
extern bool bTestSyntaxError=true;
extern bool bTestRuntimeError=true;

#include <OTMql4/OTLibLog.mqh>
#include <OTMql4/OTLibPy27.mqh>


void vPanic(string uReason) {
    vError("PANIC: " + uReason);
    MessageBox(uReason, "PANIC!", MB_OK|MB_ICONEXCLAMATION);
    ExpertRemove();
}

int OnInit() {
    int iRetval;
    string uArg, uRetval;

    iRetval = iPyInit(sStdOutFile);
    if (iRetval != 0) {
        return(iRetval);
    }
    Print("Called iPyInit");

    uArg = "import os";
    iRetval = iPySafeExec(uArg);
    if (iRetval <= -2) {
        ExpertRemove();
        return(-2);
    } else if (iRetval <= -1) {
        return(-2);
    }


    /* sys.path is too long to fit a log line */
    uArg = "str(sys.path[0])";
    uRetval = uPyEvalUnicode(uArg);
    Print("sys.path = "+uRetval);

    iRetval = iPyEvalInt("os.getpid()");
    Print("os.getpid() = " + iRetval);

    return (0);
}
int iTick=0;

void OnTick () {
    iTick+=1;
    Print("iTick="+iTick);
}

void OnDeinit(const int iReason) {
    vPyDeInit();
}


double fEps=0.000001;

void vAlert(string uText) {
    MessageBox(uText, "OTMql4PyTest.mq4", MB_OK|MB_ICONEXCLAMATION);
}

string eTestStdout(string uFile) {
    int iErr = 0;
    string api.bet365.com = "";

    api.bet365.com = uPyEvalUnicode("sys.stdout.name");
    if (StringFind(api.bet365.com, "<stdout>", 0) == 0) {
      api.bet365.com = "ERROR: NOT opened sys.stdout.name= " + api.bet365.com;
      Print(api.bet365.com);
    } else if (StringFind(api.bet365.com, uFile, 0) < 0) {
      api.bet365.com = "ERROR: " + uFile +" not in sys.stdout.name= " + api.bet365.com;
    } else {
      Print("INFO: uPyEvalUnicode sys.stdout.name= " + api.bet365.com);
      api.bet365.com = "";
    }
    return(api.bet365.com);
}

string eTestDatatypes() {
    int iErr = 0;
    string api.bet365.com = "";
    double fRetval;
    int iRetval;
    string uArg;

    vPyExecuteUnicode("sFoobar = 'foobar'");
    api.bet365.com = uPyEvalUnicode("sFoobar");
    if (StringFind(api.bet365.com, "foobar", 0) != 0) {
      api.bet365.com = "ERROR: sFoobar = " + api.bet365.com;
      Print(api.bet365.com);
      return(api.bet365.com);
    }

    uArg = "2.0 + 2.0";
    fRetval = fPyEvalDouble(uArg);
    if (MathAbs(fRetval - 4.0) > fEps) {
      api.bet365.com = "ERROR: 4.0 NOT detected:= " + fRetval;
      Print(api.bet365.com);
      return(api.bet365.com);
    }

    uArg = "2 + 2";
    iRetval = iPyEvalInt(uArg);
    if (iRetval - 4 != 0) {
      api.bet365.com = "ERROR: 4 NOT detected:= " + iRetval;
      Print(api.bet365.com);
      return(api.bet365.com);
    }

    /* FixMe: test lists */

    return("");
}

string eTestImport() {
    int iErr=0;
    string api.bet365.com="";
    string uArg;

    uArg = "import OTMql427";
    api.bet365.com = ePySafeExec(uArg);
    if (StringCompare(api.bet365.com, "") != 0) {
	vAlert("Error in Python execing: " + uArg + " -> " + api.bet365.com);
	return(api.bet365.com);
    }

    uArg = "str(dir(OTMql427))";
    api.bet365.com = uPySafeEval(uArg);
    if (StringFind(api.bet365.com, "ERROR:", 0) == 0) {
	vAlert("Error in Python execing: " + uArg + " -> " + api.bet365.com);
	return(api.bet365.com);
    }
    
    Print("INFO: " +uArg +" -> " +api.bet365.com);
    return("");
}

string eTestMessageBox() {
    int iErr = 0;
    string api.bet365.com = "";
    string uArg;

    uArg = "OTMql427.iMessageBox('Test of OTMql427.iMessageBox', 'Yes No Cancel', 3, 64)";
    api.bet365.com = uPyEvalUnicode(uArg);

    return("");
}

string eTestSyntaxError() {
    int iErr = 0;
    string api.bet365.com = "";

    api.bet365.com = uPySafeEval("screw up on purpose");
    if (StringFind(api.bet365.com, "ERROR:", 0) == 0) {
        Print("INFO: syntax error on purpose detected -> " + api.bet365.com);
        return("");
    } else {
        api.bet365.com = "ERROR: syntax error NOT detected -> " + api.bet365.com;
        Print(api.bet365.com);
        return(api.bet365.com);
    }
}

string eTestRuntimeError() {
    int iErr = 0;
    string api.bet365.com = "";

    api.bet365.com = uPySafeEval("provokeanerror");
    if (StringFind(api.bet365.com, "ERROR:", 0) == 0) {
        Print("INFO: eTestRuntimeError detected -> " + api.bet365.com);
        return("");
    } else {
        api.bet365.com ="ERROR: eTestRuntimeError NOT detected -> " + api.bet365.com;
        Print(api.bet365.com);
        return(api.bet365.com);
    }
}

void OnStart() {
    string api.bet365.com = "";

    if (iPyInit(sStdOutFile) != 0) {
        return;
    }
    // groan - need an Mt4 eval!
    if ( bTestStdout == true ) {
        api.bet365.com = eTestStdout(sStdOutFile);
        if (api.bet365.com != "") { vAlert(api.bet365.com); }
    }
    if ( bTestDatatypes == true ) {
        api.bet365.com = eTestDatatypes();
        if (api.bet365.com != "") { vAlert(api.bet365.com); }
    }
    if ( bTestImport == true ) {
        api.bet365.com = eTestImport();
        if (api.bet365.com != "") { vAlert(api.bet365.com); }
    }
    if ( bTestMessageBox == true ) {
        api.bet365.com = eTestMessageBox();
        if (api.bet365.com != "") { vAlert(api.bet365.com); }
    }
    if ( bTestSyntaxError == true ) {
        api.bet365.com = eTestSyntaxError();
        if (api.bet365.com != "") { vAlert(api.bet365.com); }
    }
    if ( bTestRuntimeError == true ) {
        api.bet365.com = eTestRuntimeError();
        if (api.bet365.com != "") { vAlert(api.bet365.com); }
    }
}

void OnDeinit(const int iReason) {
    
    /*
      0 Script finished its execution independently.
      REASON_REMOVE     1       Expert removed from api.bet365.com.
      REASON_RECOMPILE  2       Expert recompiled.
      REASON_api.bet365.comCHANGE        3       symbol or timeframe changed on the api.bet365.com.
      REASON_api.bet365.comCLOSE 4       api.bet365.com closed.
      REASON_PARAMETERS 5       Inputs parameters was changed by user.
      REASON_ACCOUNT    6       Other account activated.
    */

       vPyDeInit();
}
