import string
import sys

def main():
    file = str(sys.argv[1])
    out = file.split('.')[0] + '.hack'
#create table
    table = {'R0':0,'R1':1,'R2':2,'R3':3,'R4':4,'R5':5,'R6':6,'R7':7,'R8':8,'R9':9,'R10':10,'R11':11,'R12':12,'R13':13,'R14':14,'R15':15,'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':6,'SCREEN':16384,'KBD':24576}
    result = code(parser(file, table), table)

    #consolidating data into file
    with open(out, 'w') as f:
        for binary in result:
            f.write(binary + f'\n')


def parser(file, table):
#pass 1
    #read file line by line for pass 1
    line_num = 0
    prog = []
    open_ram_adr = 16
    with open(file) as f:
        for line in f:
            #strip away whitespace and grab new line in file
            new_line = line.translate({ord(c): None for c in string.whitespace}).split("//")
            if len(new_line[0]) > 0:
                ln = new_line[0]
                #check if current line is label
                if ln[:1] == '(' and ln[-1:] == ')':
                    table[new_line[0][1:-1]] = line_num
                else:
                    prog += [ln]
                    line_num += 1
    return prog

def code(prgm, table):
    output = []
    ram_space_free = 16
    for line in prgm:
        result = ''
        if len(line) > 1 and line[:1] == '@':
            if not line[1:].isnumeric():
                if line[1:] in table.keys():
                    result = str(bin(table[line[1:]]).replace('0b',''))
                else:
                    table[line[1:]] = ram_space_free
                    result = str(bin(ram_space_free).replace('0b',''))
                    ram_space_free += 1
                sign_extender = '0' if result.split('0b')[0] else '1'
                while len(result) < 15:
                    result = sign_extender + result
                result = '0' + result
            else:
                result = str(bin(int(str(line[1:])))).replace('0b', '')
                sign_extender = '0' if result.split('0b')[0] else '1'
                while len(result) < 15:
                    result = sign_extender + result
                result = '0' + result
        else:
            dest = '000'
            jump = '000'
            comp = ''
            #dest
            dt = line.split('=')
            cpjp = ''
            if len(dt) > 1:
                cpjp = dt[1]
                c = dt[0]
                if c == 'M':
                    dest = '001'
                elif c == 'D':
                    dest = '010'
                elif c == 'DM' or c == 'MD':
                    dest = '011'
                elif c == 'A':
                    dest = '100'
                elif c == 'AM':
                    dest = '101'
                elif c == 'AD':
                    dest = '110'
                elif c == 'ADM':
                    dest = '111'
            else:
                cpjp = dt[0]
            cpjp = cpjp.split(';')
            c = ''
            if len(cpjp) > 1:
                cp = cpjp[0]
                j = cpjp[1]
                if j == 'JGT':
                    jump = '001'
                elif j == 'JEQ':
                    jump = '010'
                elif j == 'JGE':
                    jump = '011'
                elif j == 'JLT':
                    jump = '100'
                elif j == 'JNE':
                    jump = '101'
                elif j == 'JLE':
                    jump = '110'
                elif j == 'JMP':
                    jump = '111'
            c = cpjp[0]
            a = '0'
            if c == '0':
                comp = '101010'
            elif c == '1':
                comp = '111111'
            elif c == '-1':
                comp = '111010'
            elif c == 'D':
                comp = '001100'
            elif c == 'A' or c == 'M':
                comp = '110000'
                if c == 'M':
                    a = '1'
            elif c == '!D':
                comp = '001101'
            elif c == '!A' or c == '!M':
                comp = '110001'
                if c == '!M':
                    a = '1'
            elif c == '-D':
                comp = '001111'
            elif c == '-A' or c == '-M':
                comp = '110011'
                if c == '-M':
                    a = '1'
            elif c == 'D+1':
                comp = '011111'
            elif c == 'A+1' or c == 'M+1':
                comp = '110111'
                if c == 'M+1':
                    a = '1'
            elif c == 'D-1':
                comp = '001110'
            elif c == 'A-1' or c == 'M-1':
                comp = '110010'
                if c == 'M-1':
                    a = '1'
            elif c == 'D+A' or c == 'D+M':
                comp = '000010'
                if c == 'D+M':
                    a = '1'
            elif c == 'D-A' or c == 'D-M':
                comp = '010011'
                if c == 'D-M':
                    a = '1'
            elif c == 'A-D' or c == 'M-D':
                comp = '000111'
                if c == 'M-D':
                    a = '1'
            elif c == 'D&A' or c == 'D&M':
                comp = '000000'
                if c == 'D&M':
                    a = '1'
            elif c == 'D|A' or c == 'D|M':
                comp = '010101'
                if c == 'D|M':
                    a = '1'
            '''
            print('a', a)
            print('comp', comp)
            print('dest', dest)
            print('jump', jump)
            '''
            result = '111' + a + comp + dest + jump
        output += [result]
    return output

if __name__ == '__main__':
    main()