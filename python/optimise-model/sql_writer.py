import sqlite3

from os.path import isfile


class SqlWriter(object):

    def __init__(self, options):
        self.db_file = options.db
        self.eval_no = str(options.evaluations)
        self.is_split = str(options.is_split)
        self.mul_init = str(options.mul_init)
        self.prop_no = str(options.prop_no)
        self.symm = str(options.symm)
        self.decision = None
        self.create_tables()

    def create_tables(self):
        CREATE_PRISM_TABLE = """
		CREATE TABLE IF NOT EXISTS prismdata (
		"trial_num" INTEGER NOT NULL PRIMARY KEY,
		"result"	TEXT,
		"profile1"	TEXT,
		"profile2"	TEXT,
		"profile3"	TEXT,
		"clientcount"	TEXT,
		"connectrates"	TEXT,
		"clientinit"	TEXT,
		"serverinit"	TEXT
		)
		"""

        CREATE_INFO_TABLE = """
		CREATE TABLE IF NOT EXISTS experiment (
		"evaluations" TEXT,
		"splitworld" TEXT,
		"multiplestates" TEXT,
		"propertyno" TEXT,
		"symmreduction" TEXT
		)
		"""

        INSERT_EXPERIMENT_DATA = """
		INSERT INTO experiment (
		evaluations,
		splitworld,
		multiplestates,
		propertyno,
		symmreduction)
		VALUES (?, ?, ?, ?, ?);
		"""

        if not isfile(self.db_file):
            f = open(self.db_file, 'w')
            f.close()
        else:
            while True:
                self.decision = input('Existing database already exists. Overwrite (y/n)? ')
                if self.decision == 'y' or self.decision == 'n':
                    break
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            if self.decision == 'y':
                c.execute("DELETE FROM experiment;")
                c.execute("DELETE FROM prismdata;")
            c.execute(CREATE_PRISM_TABLE)
            c.execute(CREATE_INFO_TABLE)
            values = (self.eval_no, self.is_split, self.mul_init,
                      self.prop_no, self.symm, )
            c.execute(INSERT_EXPERIMENT_DATA, values)
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close()

    def write_data(self, values):
        QUERY = """
		INSERT INTO prismdata (
		trial_num,
		result,
		profile1,
		profile2,
		profile3,
		clientcount,
		connectrates,
		clientinit,
		serverinit) 
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
		"""

        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute(QUERY, values)
        except sqlite3.Error as e:
            print(e)
        finally:
            # commit changes and close
            conn.commit()
            conn.close()

