import re
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True, description='Sample Commandline')

    parser.add_argument(
        '--file',
        action="store",
        help="path of file to take as input",
        nargs="?",
        metavar="file")

    args = parser.parse_args()

    print(args.file)
    file_input = args.file
    file_out = open("task_2_2_result.txt", "a")
    g = 0
    startState = "q0"
    stringState = "q0,q1,q2,q3,q4"
    stringTrans = "(q0, , q1), (q1, s, q2), (q1, t, q3), (q2, , q4), (q3, t, q4),(q1, , q4),(q2,s,q3)"
    alpha = " , s, t"
    acceptStates = "q4 "
    with open(file_input, 'r') as f:
        lines = f.readlines()
        stringState = lines[0].strip()

        alpha = lines[1].strip()

        startState = lines[2].strip()

        acceptStates = lines[3].strip()

        stringTrans = lines[4].strip()

        epsClosure = {}
        NFAstates = []
        isAcceptState = []
        DFAStates = []
        DFAtransitions = []
        DEADSTRING = False
        decasc = 65
        boolArrayDFAAcceptState = []

        alphas = alpha.split(",")
        alphas = [value.strip() for value in alphas]
        print("alpha", alpha)
        print("alphaS", alphas)
        NFAaccpetStates = acceptStates.split(",")
        NFAaccpetStates = [value.strip() for value in NFAaccpetStates]
        states = stringState.split(",")
        states = [value.strip() for value in states]
        trans = re.findall(r'((?<=\().*?(?=\)))', stringTrans)
        alphaTrans = {}

        def inil():
            global NFAaccpetStates
            global alphas
            global states
            global trans
            p = 0

            for state in states:
                epsClosure[state] = []
                alphaTrans[state] = {}
                for alphabet in alphas:
                    if alphabet != '':
                        alphaTrans[state][alphabet] = []

            for tran in trans:
                ss = tran.split(",")
                ss = [value.strip() for value in ss]
                if ss[1] == '':
                    epsClosure[ss[0]].append(ss[2])
                else:
                    alphal = ss[1]
                    if alphal != '':
                        alphaTrans[ss[0]][alphal].append(ss[2])

        def getepClo(nameSate, arrayStates):
            arrayStates.append(nameSate)
            i = 0
            while i < len(arrayStates):
                state = arrayStates[i]
                if len(epsClosure[state]) > 0:
                    for epsState in epsClosure[state]:
                        if epsState not in arrayStates:
                            arrayStates.append(epsState)
                i += 1
            return arrayStates

        def getNextStates():
            global decasc
            global NFAstates
            global alphaTrans
            global DFAStates
            global DFAtransitions
            dead = False
            newState = []
            j = 0
            while j < len(NFAstates):
                arrayNFAStates = NFAstates[j]
                for letter in alphas:
                    if letter != '':
                        dead = False
                        exists = False
                        arrayNextTrans = []
                        newState = []
                        for state in arrayNFAStates:
                            arrayNextTrans = alphaTrans[state][letter]
                            if len(arrayNextTrans) > 0:
                                newState = newState + arrayNextTrans

                        if len(newState) == 0:
                            dead = True
                        if not dead:
                            i = 0
                            while i < len(newState):
                                epsclosState = getepClo(newState[i], [])
                                for epsState in epsclosState:
                                    if epsState not in newState:
                                        newState.append(epsState)
                                i += 1
                            for nfaState in NFAstates:
                                setNfa = set(nfaState)
                                interscet = setNfa.intersection(newState)
                                if nfaState == newState:
                                    exists = True
                                    break
                            if not exists:
                                NFAstates.append(newState)
                                DFAStates.append(chr(decasc))
                                dfaFromStateidx = NFAstates.index(
                                    arrayNFAStates)
                                decasc += 1
                                tobeAppend = "( " + DFAStates[
                                    dfaFromStateidx] + ", " + letter + ", " + DFAStates[
                                        -1] + "" + " )"
                                DFAtransitions.append(tobeAppend)
                            elif exists:
                                DFAStateidx = NFAstates.index(newState)
                                DFAStateidxFrom = NFAstates.index(
                                    arrayNFAStates)
                                tobeAppend = "( " + DFAStates[
                                    DFAStateidxFrom] + ", " + letter + ", " + DFAStates[
                                        DFAStateidx] + "" + " )"
                                DFAtransitions.append(tobeAppend)

                        else:
                            global DEADSTRING
                            DEADSTRING = True
                            DFAStateidx = NFAstates.index(arrayNFAStates)
                            tobeAppend = "( " + DFAStates[
                                DFAStateidx] + ", " + letter + " ," + "DEAD )"
                            DFAtransitions.append(tobeAppend)

                            tobeAppend = "( " + 'DEAD ' + ", " + letter + " ," + "DEAD )"
                            if tobeAppend not in DFAtransitions:
                                DFAtransitions.append(tobeAppend)
                            for f in alphas:
                                if f != '':
                                    tobeAppend = "( " + 'DEAD ' + ", " + f + " ," + "DEAD )"
                                    if tobeAppend not in DFAtransitions:
                                        DFAtransitions.append(tobeAppend)

                j += 1

        def submitPrint():
            intAlpha = 65
            strAlpha = ""
            while intAlpha < decasc:
                strAlpha = strAlpha + chr(intAlpha) + " ,"
                intAlpha += 1

            if DEADSTRING:
                strAlpha = strAlpha + "DEAD"
            file_out.write(strAlpha)
            file_out.write("\n")
            StringALPHAS = ""
            for x in alphas:
                StringALPHAS = StringALPHAS + x + " ,"
            file_out.write(StringALPHAS)
            file_out.write("\n")
            file_out.write(DFAStates[0])
            file_out.write("\n")
            p = 0
            stringAcceptStates = ""
            while p < len(NFAstates):
                for aState in NFAaccpetStates:
                    if aState in NFAstates[p]:
                        stringAcceptStates = stringAcceptStates + DFAStates[
                            p] + " , "
                p += 1
            file_out.write(stringAcceptStates)
            file_out.write("\n")
            STRINGTRANS = ""
            for ss in DFAtransitions:
                STRINGTRANS = STRINGTRANS + ss + " , "
            file_out.write(STRINGTRANS)

        inil()
        NFAepsStateState = getepClo(startState, [])
        NFAepsStateState = set(NFAepsStateState)
        NFAepsStateState = list(NFAepsStateState)
        NFAstates.append(NFAepsStateState)
        DFAStates.append(chr(decasc))
        decasc += 1
        getNextStates()
        submitPrint()
