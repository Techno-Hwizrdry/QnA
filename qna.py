from argparse import ArgumentParser
from datetime import datetime
from secrets import MYSQL_USER, MYSQL_PASSWD

import MySQLdb
import sys

HOST = "192.168.1.195"
DATABASE_NAME = "QnA"

db  = MySQLdb.connect(host=HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=DATABASE_NAME)
cur = db.cursor()

class QnAArgParser(ArgumentParser):
        def error(self, message):
                sys.stderr.write('error: %s\n' %message)
                self.print_help()
                sys.exit(2)

def get_args():
        parser = QnAArgParser()

        parser.add_argument('-t', dest='question_text', help='The text needed to add a new question or change an existing one.')
        parser.add_argument('-c', dest='changed_question_text', help='The text need to change an existing question.')
        parser.add_argument('-d', action="store_true", dest='show_diff', help='Display diff of changes to question text over time.')

        if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
                parser.print_help()
                sys.exit(1)

        return parser.parse_args()

def addNewQuestion(new_text):
        try:
                sql = "INSERT INTO questions (question) VALUES (%s);"
                cur.execute(sql, (new_text,))
        except MySQLdb.IntegrityError:
                print "This question already exists in the QnA database."

def getQuestionID(question_text):
        sql = "SELECT id FROM questions WHERE question=%s";
        cur.execute(sql, (question_text,))

        results = None

        try:
                results = cur.fetchall()[0][0]
        except IndexError:
                results = False

        return results

def addQuestionChange(original_question_text, changed_text):
        original_question_id = getQuestionID(original_question_text)

        if original_question_id == False:
                print "ERROR: Cannot add a change for a non-existant question.  Question \'%s\' does not exist." % (original_question_text)
        else:
                try:
                        sql = "INSERT INTO question_changes (question_id, changed_text) VALUES (%s, %s);"
                        cur.execute(sql, (original_question_id, changed_text))
                except MySQLdb.IntegrityError:
                        print "This question change already exists in the QnA database."

def printQuestionDiff(question_id):
        sql = "SELECT * FROM questions WHERE id=%s;"
        cur.execute(sql, (question_id))
        questions_results = cur.fetchall()

        if len(questions_results) == 0:
                print "No results for question ID %s" % (question_id)

        print "results: " + str(cur.fetchall())

def printQuestionDiffStr(question_text):
        CHANGEDTEXT_INDEX = 0
        TIMESTAMP_INDEX   = 1

        question_id = getQuestionID(question_text)

        if question_id == False:
                print "ERROR: Cannot display diff for the non-existant question \'%s\' ." % (question_text)
        else:
                sql = "SELECT changed_text, timestamp FROM question_changes WHERE question_id=%s";
                cur.execute(sql, (question_id,))
                results = cur.fetchall()

                # Print a nice header for the output.  :)
                print question_text
                print '-' * len(question_text)

                if len(results) == 0:
                        print "There are no changes for this question."
                else:
                        for result in results:
                                print str(result[TIMESTAMP_INDEX]) + "\t" + result[CHANGEDTEXT_INDEX]

def main():
        opts = get_args()

        if not opts.question_text:
                print "No question text provided.  Please use the -t switch."
                sys.exit(1)

        if opts.changed_question_text:
                addQuestionChange(opts.question_text, opts.changed_question_text)
        elif opts.show_diff:
                printQuestionDiffStr(opts.question_text)
        else:
                addNewQuestion(opts.question_text)

        db.commit()

if __name__ == '__main__':
        main()