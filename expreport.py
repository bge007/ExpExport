#!/usr/bin/python

import re
import sys
import urllib
# import collections
import base64
# import numpy as np


def file_write(config, fname, ftype):
    rowvalue = ""
    with open(fname+'.'+ftype, 'w') as myfile:
        # myfile.write('<html>')
        # myfile.write('<body style="background-color:#3D3634;">\r\n')
        if(ftype == "html"):
            myfile.write('<body style="background-color:white;">\r\n')
            myfile.write('<body">\r\n')
            # myfile.write('<table border=1>\r\n')

        newtable = "<table border=1>\n"
        closetable = "</table>\n"

        idx = 0
        # msg = ""
        # while idx < len(config):  ###### enable loop here..
        while idx < len(config):  # remove after testing...
            if (ftype == "html"):
                headrow = '\n\t<tr><td>' + config[idx][0] + '</td>'
            else:
                headrow = '\n\t' + config[idx][0] + "\t"

            col = 0  # to have the value of "j" start from 0 as "i" may not be 0 always...
            # vcol = 0
            valrow = ""
            if idx+1 < len(config) and config[idx][2].isdigit() and config[idx][2] == config[idx+1][2]:
                while idx+col <= len(config) and config[idx+col][2].isdigit() and int(config[idx][2]) == int(config[idx+col][2]):
                    if (ftype == "html"):
                        headrow = headrow + "\t\t<td>" + config[idx + col][1] + "</td>"
                    else:
                        headrow = headrow + "\t" + config[idx + col][1] + "\t"

                    col = col + 1
                # grplst = 0
                # print config[idx][2]
                # print config[idx+1][2]
                rowvalue = ""
                # while idx+1<=len(config) and int(config[idx][2]) <= int(config[idx+1][2]):  ##Logic error......
                while idx+1 <= len(config) and config[idx][2].isdigit() and config[idx+1][2].isdigit() and int(config[idx][2]) <= int(config[idx+1][2]):
                    # print "NNN:" + str(type(int(config[idx+1][2]))) + " - " + str(int(config[idx+1][2]))
                    # while idx+1<=len(config) and int(config[idx][2]) <= int(config[idx+1][2]):
                    i = int(config[idx][2])
                    # print ('%s \t %s' % (config[idx][2], config[idx+1][2]))
                    # ////to do from here for the table row population....
                    if (ftype == "html"):
                        valrow = "\n\t\t<tr><td>"+config[idx][2]+" </td>"
                    else:
                        valrow = "\n\t"+config[idx][2] + "\t"

                    while idx < len(config) and config[idx][2].isdigit() and i == int(config[idx][2]):
                        if (ftype == "html"):
                            valrow = valrow + "\t\t<td>" + \
                                urllib.unquote(str(config[idx][3])).replace(
                                    '\n', '<br>\n') + "</td>\r\n"
                        else:
                            valrow = valrow + "\t" + \
                                urllib.unquote(str(config[idx][3])) + "\t"
                        idx = idx + 1

                    if (ftype == "html"):
                        valrow = valrow + "</tr>"
                    else:
                        valrow = valrow + "\n\t"

                    rowvalue = rowvalue + valrow

                    if idx < len(config) and config[idx][2].isdigit() and int(config[idx-1][2]) > int(config[idx][2]):
                        break
                if(ftype == "html"):
                    conftable = newtable + headrow + rowvalue + closetable + "<br>"
                else:
                    conftable = headrow + rowvalue + "\n"
                myfile.write('%s\r\n' % urllib.unquote(conftable))
            else:
                if(ftype == "html"):
                    rowvalue = "\n\t\t<tr><td>" + str(config[idx][1]) + "&nbsp;</td><td>" + str(
                        config[idx][2]) + "&nbsp;</td><td> " + str(config[idx][3]).replace('\n', '<br>\n')+"&nbsp;</td></tr>"
                else:
                    rowvalue = "\n\t" + str(config[idx][1]) + "\t" + str(
                        config[idx][2]) + "\t" + str(config[idx][3]) + "\n"
                idx = idx + 1

                if(ftype == "html"):
                    conftable = newtable + rowvalue + closetable + "<br>"
                else:
                    conftable = rowvalue + "\n"

                myfile.write('%s\r\n' % urllib.unquote(conftable))

        if(ftype == "html"):
            myfile.write('</body>')
            myfile.write('</html>\r\n')

    myfile.close()
    print "Written to: " + fname + "." + ftype


def arrayfy(decoded_data):
    config = []
    for index in range(len(decoded_data)-1):
        ddata = decoded_data[index]
        # print "::"+str(index)
        # varnval = ddata.split("_")
        # maximum split to 1 for avoiding any value part containing text with "=" sign
        varnval = ddata.split("=", 1)

        if not varnval:
            var = "EMPTYVAR_AAA"  # just placeholder to check
            val = "EMPTYVAL_AAA"  # just placeholder to check

        elif len(varnval) == 2:
            var, val = varnval  # split configuration variable and its value by spliting on "="

        elif type(varnval) == list:
            var = "LIST_AAAA"  # just placeholder to check
            val = "AAAAAAAAA" + ", ".join(varnval)  # just placeholder to check

        else:
            var = "UNKNOWN_AAAAA"  # just placeholder to check
            val = "AAAAAAAAAAAAA" + varnval  # just placeholder to check

        grp_conf = var.split("_")

        if len(grp_conf) == 1:
            confgrp = ""
            conftyp = var  # grp_conf[0]
            confnum = ""

        elif len(grp_conf) == 2:
            confgrp = ""
            conftyp, confnum = grp_conf

            if type(confnum) == str:
                confgrp = conftyp
                conftyp = confnum
                confnum = ""

            # print conftyp + " yyyy " + str(type(conftyp))
            if conftyp.isdigit():
                confnum = conftyp
                conftyp = confgrp
                if re.match('^schedObj', conftyp):
                    confgrp = "schedObj"
                elif re.match('^zoneObj', conftyp):
                    confgrp = "zoneObj"
                elif re.match('^wgsSocial', conftyp):
                    confgrp = "zoneObj"
                elif re.match('^addrObjV6', conftyp):
                    confgrp = "addrObjV6"
                elif re.match('^addrObj', conftyp):
                    confgrp = "addrObj"
                elif re.match('^svcObj', conftyp):
                    confgrp = "svcObj"
                elif re.match('^userObj', conftyp):
                    confgrp = "userObj"
                elif re.match('^userGroupObj', conftyp):
                    confgrp = "userGroupObj"
                elif re.match('^bwObj', conftyp):
                    confgrp = "bwObj"
                elif re.match('^cfsPolicy', conftyp):
                    confgrp = "cfsPolicy"
                elif re.match('^cfsCustomCategory', conftyp):
                    confgrp = "cfsCustomCategory"
                elif re.match('^cfs', conftyp):
                    confgrp = "cfs"
                elif re.match('^lldpProf', conftyp):
                    confgrp = "lldpProf"
                elif re.match('^auxSyslog', conftyp):
                    confgrp = "auxSyslog"
                elif re.match('^logPrefs', conftyp):
                    confgrp = "logPrefs"
                elif re.match('^logCtgr', conftyp):
                    confgrp = "logCtgr"
                elif re.match('^logTemp', conftyp):
                    confgrp = "logTemp"
                elif re.match('^rbl', conftyp):
                    confgrp = "rbl"
                elif re.match('^partAuth', conftyp):
                    confgrp = "partAuth"
                elif re.match('^ldapSrvr', conftyp):
                    confgrp = "ldapSrvr"
                elif re.match('^ldapUsrs', conftyp):
                    confgrp = 'ldapUsrs'
                elif re.match('^ldapUsrGrps', conftyp):
                    confgrp = 'ldapUsrGrps'
                elif re.match('^ldapAllow', conftyp):
                    confgrp = 'ldapAllow'
                elif re.match('^ldapMirror', conftyp):
                    confgrp = 'ldapMirror'
                elif re.match('^userAcct', conftyp):
                    confgrp = 'userAcct'
                elif re.match('^autoLognBypass', conftyp):
                    confgrp = 'autoLognBypass'
                elif re.match('^autoLognWinSvc', conftyp):
                    confgrp = 'autoLognWinSvc'
                elif re.match('^addCustomNTP', conftyp):
                    confgrp = 'NTPServer'
                elif re.match('^NTPServer', conftyp):
                    confgrp = 'NTPServer'
                elif re.match('^idp', conftyp):
                    confgrp = 'idp'
                elif re.match('^ZOspf3', conftyp):
                    confgrp = 'ZOspf3'
                elif re.match('^swZOspf3', conftyp):
                    confgrp = 'ZOspf3'
                elif re.match('^swRip', conftyp):
                    confgrp = 'swRip'
                elif re.match('^ZOspf', conftyp):
                    confgrp = 'ZOspf'
                elif re.match('^swZOspf', conftyp):
                    confgrp = 'ZOspf'
                elif re.match('^swIsIf', conftyp):
                    confgrp = 'ZOspf'
                elif re.match('^swZRip', conftyp):
                    confgrp = 'swZRip'
                elif re.match('^ZRip', conftyp):
                    confgrp = 'swZRip'
                else:
                    confgrp = "aaaaa"

        elif len(grp_conf) > 2:
            conflst = var.split("_", 1)
            confgrp = conflst[0]
            conflst = conflst[1].rsplit("_", 1)
            # confnum = conflst[1].split("_")[-1]
            conftyp = conflst[0]
            confnum = conflst[1]

        # print ddata + "\t" + confgrp + "\t" + conftyp + "\t" + confnum + "\t" + val
        # print confgrp + "\t" + conftyp + "\t" + confnum + "\t" + val

        config.append([])
        config[index].append(confgrp)
        config[index].append(conftyp)
        config[index].append(confnum)
        config[index].append(val)

        # prev_confgrp = confgrp  # previous group config
        # prev_conftyp = conftyp  # previous config type
        # prev_confnum = confnum  # previous row number of the group configuration
        # prev_val = val  # previous vaule of the configuration
    return(config)


def main():
    decoded_data = []
    if re.search('\.exp$', sys.argv[1], re.IGNORECASE):
        with open(sys.argv[1], 'r') as f:
            read_data = f.readline()
        f.close()
        decoded_str = base64.b64decode(read_data)
        decoded_data = decoded_str.split("&")

    else:
        file = open(sys.argv[1], 'r')
        ii = 0
        for line in file:
            decoded_data.append(line.rstrip("\n\r"))
            # print str(i)+ " - " + decoded_data[i]
            ii += 1
        file.close()

    # sys.exit()
    fname = sys.argv[1]

    # print len(decoded_data)
    # print type(decoded_data)
    # print "confgrp" + "\t" + "conftyp" + "\t" + "confnum" + "\t" + "val"

    config = arrayfy(decoded_data)
    file_write(config, fname, "html")
    file_write(config, fname, "txt")


if __name__ == '__main__':
    main()
