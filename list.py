#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import getopt
import time
import os,sys
from record import Record
from utils import Utils
import copy

source = ""
filter_keyword = ""
column_num = "2"

custom_cell_len = 0
custom_cell_row = 5
cell_len=89  #  cell_len >= course_num_len + 1 + course_name_len + 3
course_name_len=70
course_num_len=10
color_index=0
output_with_color = False
output_with_describe = False

utils = Utils()
line_max_len_list = [0, 0, 0]
line_id_max_len_list = [0, 0, 0]

keyword_list = ['videourl:', 'author:', 'ratings:', 'term:', 'prereq:', 'toprepo:', 'project:', 'university:', 'available:', 'level:', 'features:', 'instructors:', 'description:', 'textbook:']


def usage():
    print 'usage:'
    print '\t-h,--help: print help message.'
    print '\t-k,--keyword: print suggest keyword in file.'
    print '\t-i,--input: filename or dirname'
    print '\t-c,--column: from 1 to 3'
    print '\t-f,--filter: keyword for filter course'
    print '\t-s,--style: print text with color'
    print '\t-d,--describe: output the describe of the item'
    print '\t-w,--width: the width of cell'
    print '\t-r,--row: the rows of the describe'
    os.system("cat README.md")

def print_keyword(file_name):
    cmd = '\
        tr -sc "[A-Z][a-z]"  "[\012*]"  < ' + file_name + '|  \
        tr  "[A-Z]"  "[a-z]"  | \
        sort  | uniq -c |   \
        sort  -k1 -n -r  |  \
        head -50 | nl'
    os.system(cmd)

def color_keyword(text):
    result = text
    for k in keyword_list:
        if (color_index - 1) % 2 == 0:
            result = result.replace(k, utils.getColorStr('brown', k))
        else:
            result = result.replace(k, utils.getColorStr('darkcyan', k))

    return result

def align_id_title(record):
    course_num = record.get_id()
    course_name = record.get_title()
    if utils.str_block_width(course_name) > course_name_len:
        course_name = course_name[0 : course_name_len - 3 ] + "..."
    else:
        course_name = course_name + get_space(0, course_name_len - utils.str_block_width(course_name))

    if len(course_num) < course_num_len:
        space = get_space(0, course_num_len - len(course_num))
        return course_num + space + "|"+ course_name
    else:
        return course_num + "|" + course_name

def align_describe(describe):
    if utils.str_block_width(describe) > course_name_len - 1 and output_with_describe == False:
        describe = describe[0 : course_name_len - 3 ] + "..."
    else:
        describe += get_space(0, course_name_len - utils.str_block_width(describe))
    return get_space(0, course_num_len) + "|" + describe

def print_with_color(text):
    global color_index
    if color_index % 2 == 0:
        utils.print_colorful("brown", True, text)
    else:
        utils.print_colorful("darkcyan", True, text)
    color_index += 1

def print_table_head(col, id_name='id', title='title'):
    if output_with_describe == True:
        title = "detail"
    table_head_mid = ''
    for i_i in range(0, col):
        update_cell_len(i_i)
        table_head_mid += '|'
        space_1 = get_space(0, course_num_len - len(id_name))
        space_2 = get_space(0, course_name_len - len(title))
        if len(space_1) % 2 == 0 and len(space_2) % 2 == 0:
            table_head_mid += space_1[0 : len(space_1) / 2] + id_name + space_1[len(space_1) / 2 :] + '|' + space_2[0 : len(space_2) / 2] + title + space_2[len(space_2) / 2 :]
        else:
            table_head_mid += id_name + space_1 + '|' + title + space_2

    table_head_mid += '|'
    print_table_separator(col)
    print table_head_mid
    print_table_separator(col)

def print_table_separator(col):
    table_separator = ''
    for i_i in range(0, col):
        update_cell_len(i_i)
        table_separator += "+"
        for sp in range(0, course_num_len):
            table_separator += "-"
        table_separator += "+"
        for sp in range(0, course_name_len):
            table_separator += "-"
    table_separator += "+"
    print table_separator

def get_space(start, end):
    space = ""
    for j in range(start, end):
        space += " "
    return space
def get_id_and_title(record):
    return record.get_id() + "|" + record.get_title()

def update_max_len(record, col):
    if utils.str_block_width(get_id_and_title(record)) > line_max_len_list[col - 1]:
        line_max_len_list[col - 1] = utils.str_block_width(get_id_and_title(record))
    if utils.str_block_width(record.get_id()) > line_id_max_len_list[col - 1]:
        line_id_max_len_list[col - 1] = utils.str_block_width(record.get_id()) 


def update_cell_len(index):
    global cell_len, course_name_len, course_num_len
    cell_len = line_max_len_list[index]
    if custom_cell_len > 0:
        cell_len = custom_cell_len        
    course_num_len = line_id_max_len_list[index]
    if cell_len == 0 or course_num_len == 0:
        cell_len = line_max_len_list[0]
        course_num_len = line_id_max_len_list[0]
    course_name_len = cell_len - course_num_len - 1

def next_pos(text, start):
    min_end = len(text)
    for k in keyword_list:
        end = text.lower().find(k, start + 2)
        if end != -1 and end < min_end:
            min_end = end

    if min_end != len(text):
        min_end -= 1
        if min_end - start > course_name_len:
            return start + course_name_len
        else:
            return min_end

    if (len(text) - start) < course_name_len:
        return start + len(text) - start
    else:
        return start + course_name_len

def build_lines(list_all):
    id_title_lines = copy.deepcopy(list_all)
    describe_lines = []
    for i in range(0, custom_cell_row):
        describe_lines.append(copy.deepcopy(list_all))
    for i in range(0, len(list_all)):
        update_cell_len(i)

        if len(id_title_lines[i]) == 0:
            record = Record("");
            id_title_lines[i].append(align_id_title(record))
            for l in range(0, len(describe_lines)):
                describe_lines[l][i].append(align_describe(""))

        for j in range(0, len(list_all[i])):
            id_title_lines[i][j] = align_id_title(list_all[i][j])
            describe = utils.str_block_width(list_all[i][j].get_describe())
            start = 0
            end = 0
            if output_with_describe == True:
                for l in range(0, len(describe_lines)):
                    if end >= describe:
                        describe_lines[l][i][j] = align_describe("")
                        continue
                    end = next_pos(list_all[i][j].get_describe(), start) 
                    describe_lines[l][i][j] = align_describe(list_all[i][j].get_describe()[start : end])
                    start = end

    return id_title_lines, describe_lines


def get_line(lines, start, end, j):
    result = "|"
    for i in range(start, end):
        result += color_keyword(lines[i][j])+ "|"

    return result

def get_space_cell(num):
    result = ""
    for i in range(0, num):
        result += get_space(0, course_num_len) + "|" + get_space(0, course_name_len)

    return result
def reset_max_len_list():
    global line_max_len_list, line_id_max_len_list
    line_max_len_list = [0, 0, 0]
    line_id_max_len_list = [0, 0, 0]

def print_list(file_name):
    current = 0
    old_line = ""
    old_line_2 = ""
    color_index = 0
    if os.path.exists(file_name):

        f = open(file_name,'rU')
        all_lines = f.readlines()
        if filter_keyword != "":
            filter_result = []
            for line in all_lines:
                record = Record(line)
                data = record.get_id() + record.get_title() #+ record.get_describe()
                if data.lower().find(filter_keyword.lower()) != -1:
                    filter_result.append(line)
            all_lines = filter_result[:]
        if len(all_lines) == 0:
            return  
        line_count = len(all_lines)
        list_all = []
        reset_max_len_list()
 
        line_half = 0
        if column_num == "3":
            list_all.append([])
            list_all.append([])
            list_all.append([])
            line_half = line_count / 3
        elif column_num == "2":
            list_all.append([])
            list_all.append([])
            line_half = line_count / 2
        elif column_num == "1":
            list_all.append([])
         
        for line in all_lines:
            line = utils.to_unicode(line)
            record = Record(line.replace("\n", ""))
            current += 1
            if column_num == "3":
                if current <= line_half + (line_count % 3):
                    update_max_len(record, 1)
                    list_all[0].append(record)
                elif current <= 2 * line_half + (line_count % 3):
                    update_max_len(record, 2)
                    list_all[1].append(record)
                else:
                    update_max_len(record, 3)
                    list_all[2].append(record)

            elif column_num == "2":
                if current <= line_half + (line_count % 2):
                    update_max_len(record, 1)
                    list_all[0].append(record)
                else:
                    update_max_len(record, 2)
                    list_all[1].append(record)
            else:
                update_max_len(record, 1)
                list_all[0].append(record)


        if column_num == "3":
            if len(list_all[0]) - len(list_all[1]) == 2:
                list_all[1].insert(0, list_all[0][len(list_all[0]) - 1])
                list_all[0].pop()

        id_title_lines, describe_lines = build_lines(list_all)

        if column_num == "3":
            print_table_head(3)
            for i in range(0, len(id_title_lines[2])):
                content = get_line(id_title_lines, 0, 3, i)
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True: 
                    for l in range(0, len(describe_lines)):
                        print get_line(describe_lines[l], 0, 3, i)

            if len(id_title_lines[0]) > len(id_title_lines[2]):
                last = len(id_title_lines[0]) - 1
                content = ""
                if len(id_title_lines[0]) == len(id_title_lines[1]):
                    content = get_line(id_title_lines, 0, 2, last) + get_space_cell(1) + "|"
                else:
                    content = get_line(id_title_lines, 0, 1, last) + get_space_cell(2) + "|"

                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:
                    for l in range(0, len(describe_lines)):
                        if len(id_title_lines[0]) == len(id_title_lines[1]):
                            print get_line(describe_lines[l], 0, 2, last) + get_space_cell(1) + "|"
                        else:
                            print get_line(describe_lines[l], 0, 1, last) + get_space_cell(2) + "|"

            print_table_separator(3)
        elif column_num == "2":
            print_table_head(2)
            for i in range(0, len(id_title_lines[1])):
                content = get_line(id_title_lines, 0, 2, i)
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:    
                    for l in range(0, len(describe_lines)):
                        print get_line(describe_lines[l], 0, 2, i)
            if len(id_title_lines[0]) > len(id_title_lines[1]):
                last = len(id_title_lines[0]) - 1
                content = get_line(id_title_lines, 0, 1, last) + get_space_cell(1) + "|"
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:
                    for l in range(0, len(describe_lines)):
                        print get_line(describe_lines[l], 0, 1, last) + get_space_cell(1) + "|"

            print_table_separator(2)
        elif column_num == '1':
            print_table_head(1)
            for i in range(0, len(id_title_lines[0])):
                content = get_line(id_title_lines, 0, 1, i)

                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:
                    for l in range(0, len(describe_lines)):
                        print get_line(describe_lines[l], 0, 1, i)

            print_table_separator(1)

        if current > 0:
            if filter_keyword != "":
                print "\nTotal " + str(current) + " records cotain " + filter_keyword + ", File: " + file_name + "\n\n"
            else:
                print "\nTotal " + str(current) + " records, File: " + file_name + "\n\n"
            

def print_dir(dir_name):
    cur_list = os.listdir(dir_name)
    for item in cur_list:
        if item.startswith("."):
            continue

        full_path = os.path.join(dir_name, item)
        if os.path.isfile(full_path):
            print_list(full_path)
        else:
            print_dir(full_path)


def main(argv):
    global source
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hk:i:c:f:sdw:r:', ["help", "keyword", "input=", "column=", "filter=", "style", "describe", "width", "row"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    global column_num,filter_keyword, output_with_color, output_with_describe, custom_cell_len, custom_cell_row
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)
        elif o in ('-k', '--keyword'):
            if os.path.isfile(a):
                print_keyword(a)
            else:
                print "please input file name"
            sys.exit(1)
        elif o in ('-i', '--input'):
            source = a
        elif o in ('-c', '--column_num'):
            column_num = a
        elif o in ('-f', '--filter'):
            filter_keyword = str(a).strip()
        elif o in ('-s', '--style'):
            output_with_color = True
        elif o in ('-d', '--describe'):
            output_with_describe = True
            if column_num == '2':
                custom_cell_len = cell_len + (cell_len / 14)
            elif column_num == '1':
                custom_cell_len = cell_len * 2
            output_with_color = True
        elif o in ('-w', '--width'):
            custom_cell_len = int(a) 
        elif o in ('-r', '--row'):
            if int(a) > 0 and int(a) < 30:
                custom_cell_row = int(a)
            else:
                print 'the row must between 0 and 30'
    if source == "":
        print "you must input the input file or dir"
        usage()
        return
    #if output_with_color == True:
    #    print "color"
    if source.lower().find(".pdf") != -1:
        os.system("open " + source)
        return

    if os.path.isfile(source):
        print_list(source)
    else:
        print_dir(source)

if __name__ == '__main__':
    main(sys.argv)



