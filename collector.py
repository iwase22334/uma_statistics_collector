#!/usr/bin/env python3

import numpy as np
import os
import psycopg2
import datetime
from tqdm import tqdm

tablename = 'uma_statistics_01'

def gen_initial_statistics():
    statistics_list = {}
    statistics_list['ruikeihonshiba'] = 0
    statistics_list['ruikeihondirt'] = 0
    statistics_list['ruikeifukashiba'] = 0
    statistics_list['ruikeifukadirt'] = 0
    statistics_list['ruikeichakukaisu'] = 0
    statistics_list['chakukaisu1'] = 0
    statistics_list['chakukaisu2'] = 0
    statistics_list['chakukaisu3'] = 0
    statistics_list['chakukaisu4'] = 0
    statistics_list['chakukaisu5'] = 0
    statistics_list['sshibachakukaisu1'] = 0
    statistics_list['sshibachakukaisu2'] = 0
    statistics_list['sshibachakukaisu3'] = 0
    statistics_list['sshibachakukaisu4'] = 0
    statistics_list['sshibachakukaisu5'] = 0
    statistics_list['rshibachakukaisu1'] = 0
    statistics_list['rshibachakukaisu2'] = 0
    statistics_list['rshibachakukaisu3'] = 0
    statistics_list['rshibachakukaisu4'] = 0
    statistics_list['rshibachakukaisu5'] = 0
    statistics_list['lshibachakukaisu1'] = 0
    statistics_list['lshibachakukaisu2'] = 0
    statistics_list['lshibachakukaisu3'] = 0
    statistics_list['lshibachakukaisu4'] = 0
    statistics_list['lshibachakukaisu5'] = 0
    statistics_list['sdirtchakukaisu1'] = 0
    statistics_list['sdirtchakukaisu2'] = 0
    statistics_list['sdirtchakukaisu3'] = 0
    statistics_list['sdirtchakukaisu4'] = 0
    statistics_list['sdirtchakukaisu5'] = 0
    statistics_list['rdirtchakukaisu1'] = 0
    statistics_list['rdirtchakukaisu2'] = 0
    statistics_list['rdirtchakukaisu3'] = 0
    statistics_list['rdirtchakukaisu4'] = 0
    statistics_list['rdirtchakukaisu5'] = 0
    statistics_list['ldirtchakukaisu1'] = 0
    statistics_list['ldirtchakukaisu2'] = 0
    statistics_list['ldirtchakukaisu3'] = 0
    statistics_list['ldirtchakukaisu4'] = 0
    statistics_list['ldirtchakukaisu5'] = 0
    statistics_list['u16shibachakukaisu1'] = 0
    statistics_list['u16shibachakukaisu2'] = 0
    statistics_list['u16shibachakukaisu3'] = 0
    statistics_list['u16shibachakukaisu4'] = 0
    statistics_list['u16shibachakukaisu5'] = 0
    statistics_list['u22shibachakukaisu1'] = 0
    statistics_list['u22shibachakukaisu2'] = 0
    statistics_list['u22shibachakukaisu3'] = 0
    statistics_list['u22shibachakukaisu4'] = 0
    statistics_list['u22shibachakukaisu5'] = 0
    statistics_list['u28shibachakukaisu1'] = 0
    statistics_list['u28shibachakukaisu2'] = 0
    statistics_list['u28shibachakukaisu3'] = 0
    statistics_list['u28shibachakukaisu4'] = 0
    statistics_list['u28shibachakukaisu5'] = 0
    statistics_list['o28shibachakukaisu1'] = 0
    statistics_list['o28shibachakukaisu2'] = 0
    statistics_list['o28shibachakukaisu3'] = 0
    statistics_list['o28shibachakukaisu4'] = 0
    statistics_list['o28shibachakukaisu5'] = 0
    statistics_list['u16dirtchakukaisu1'] = 0
    statistics_list['u16dirtchakukaisu2'] = 0
    statistics_list['u16dirtchakukaisu3'] = 0
    statistics_list['u16dirtchakukaisu4'] = 0
    statistics_list['u16dirtchakukaisu5'] = 0
    statistics_list['u22dirtchakukaisu1'] = 0
    statistics_list['u22dirtchakukaisu2'] = 0
    statistics_list['u22dirtchakukaisu3'] = 0
    statistics_list['u22dirtchakukaisu4'] = 0
    statistics_list['u22dirtchakukaisu5'] = 0
    statistics_list['u28dirtchakukaisu1'] = 0
    statistics_list['u28dirtchakukaisu2'] = 0
    statistics_list['u28dirtchakukaisu3'] = 0
    statistics_list['u28dirtchakukaisu4'] = 0
    statistics_list['u28dirtchakukaisu5'] = 0
    statistics_list['o28dirtchakukaisu1'] = 0
    statistics_list['o28dirtchakukaisu2'] = 0
    statistics_list['o28dirtchakukaisu3'] = 0
    statistics_list['o28dirtchakukaisu4'] = 0
    statistics_list['o28dirtchakukaisu5'] = 0
    statistics_list['kyakusitukubunkaisu1'] = 0
    statistics_list['kyakusitukubunkaisu2'] = 0
    statistics_list['kyakusitukubunkaisu3'] = 0
    statistics_list['kyakusitukubunkaisu4'] = 0

    return statistics_list

def increment(statistics, key):
    statistics[key] = statistics[key] + 1

def add(statistics, key, val):
    statistics[key] = statistics[key] + val

def update_statistics(statistics, race_info, kakuteijyuni_str, kyakusitukubun_str):
    trackcd     = int(race_info[RaceInfoReference.index('trackcd')])
    kakuteijyuni = int(kakuteijyuni_str)
    kyakusitukubun = int(kyakusitukubun_str)

    if kakuteijyuni == 0:
        raise RuntimeError("Unexpected kakuteijyuni: 0")

    jyunikey = str(kakuteijyuni)

    kyori = int(race_info[RaceInfoReference.index('kyori')])
    if kyori >= 1000 and kyori <= 1600:
        kyorikey = 'u16'
    elif kyori <= 2200:
        kyorikey = 'u22'
    elif kyori <= 2800:
        kyorikey = 'u28'
    elif kyori > 2800 and kyori <= 3600:
        kyorikey = 'o28'
    else:
        raise RuntimeError("Unexpected kyori type: %d" % (kyori,))

    if trackcd == 0:
        raise RuntimeError("Unexpected data shortage of trackcd")
    elif trackcd >= 10 and trackcd <= 22:
        trackkey = 'shiba'
    elif trackcd >= 23 and trackcd <= 29:
        trackkey = 'dirt'
    else:
        raise NotImplementedError("trackcd: " + str(trackcd) + " is not implemented")

    # turf
    if trackcd == 10:
        lrkey = 's'
    elif trackcd >= 11 and trackcd <= 16:
        lrkey = 'l'
    elif trackcd >= 17 and trackcd <= 22:
        lrkey = 'r'
    # dirt
    elif trackcd == 29:
        lrkey = 's'
    elif trackcd == 23 or trackcd == 25 or trackcd == 27:
        lrkey = 'l'
    elif trackcd == 24 or trackcd == 26 or trackcd == 28:
        lrkey = 'r'

    if kakuteijyuni <= 5:
        honsyokin_str = race_info[RaceInfoReference.index('honsyokin%d' % (kakuteijyuni,))]
        honsyokin = int(honsyokin_str) if not honsyokin_str is None else 0
        fukasyokin_str = race_info[RaceInfoReference.index('fukasyokin%d' % (kakuteijyuni,))]
        fukasyokin = int(fukasyokin_str) if not fukasyokin_str is None else 0

        increment(statistics, 'chakukaisu%d' % (kakuteijyuni,))
        increment(statistics, '%s%schakukaisu%d' % (lrkey, trackkey, kakuteijyuni,))
        increment(statistics, '%s%schakukaisu%d' % (kyorikey, trackkey, kakuteijyuni,))
        # syokin
        add(statistics, 'ruikeihon%s' % (trackkey,), honsyokin)
        add(statistics, 'ruikeifuka%s' % (trackkey,), fukasyokin)

    increment(statistics, 'ruikeichakukaisu')

    # kyakusitu
    if kyakusitukubun > 0:
        increment(statistics, 'kyakusitukubunkaisu%d' % (kyakusitukubun,))

class IDFilter:
    @classmethod
    def generate_phrase(cls, id):
        return " year='%s' AND monthday='%s' AND jyocd='%s' AND kaiji='%s' AND nichiji='%s' AND racenum='%s'" % id

class IDFilterUntilToday:
    @classmethod
    def generate_phrase(cls, id):
        return " concat(year, monthday)<'%s'" % (id[0] + id[1],)

class DateFilter:
    @classmethod
    def generate_condition_older(cls, yearmonthday):
        return " concat(year, monthday)>='%s'" % yearmonthday

    @classmethod
    def generate_condition_newer(cls, yearmonthday):
        return " concat(year, monthday)<='%s'" % yearmonthday

class SelectPhrase:
    @classmethod
    def generate(self, reference):
        query = 'SELECT ' + reference.cols.strip() + ' FROM ' + reference.table.strip()

        if reference.conditions.strip():
            query += ' WHERE ' + reference.conditions.strip()

        if reference.order.strip():
            query += ' ORDER BY ' + reference.order.strip()

        if reference.limit.strip():
            query += ' LIMIT ' + reference.limit.strip()

        return query

class InsertPhrase:
    @classmethod
    def generate(self, id, kettonum, statistics):
        str =  "INSERT INTO %s VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s'" % ((tablename,) + id + (kettonum,))

        for value in list(statistics.values()):
            str = str + ", '%d'" % value

        str = str + ");"
        return str

class IDListReference:
    def __init__(self, fromyearmonthday, toyearmonthday):
        self.table      = 'n_race'
        self.cols       = 'year, monthday, jyocd, kaiji, nichiji, racenum'
        self.conditions = "datakubun='7'" + ' AND' + DateFilter.generate_condition_older(fromyearmonthday) + ' AND' + DateFilter.generate_condition_newer(toyearmonthday)
        self.order      = 'year ASC, monthday ASC, jyocd ASC, nichiji ASC, racenum ASC'
        self.limit      = ''
        #self.limit      = '3'

class kettonumReference:
    __cols = 'kettonum, ijyocd'

    def __init__(self, id):
        self.table      = 'n_uma_race'
        self.cols       = kettonumReference.__cols
        self.conditions = IDFilter.generate_phrase(id) + " AND datakubun='7'"
        self.order      = 'kettonum DESC'
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class HorseInfoReference:
    __cols =  'year, monthday, jyocd, kaiji, nichiji, racenum, ijyocd, kakuteijyuni, kyakusitukubun'

    def __init__(self, id, fromymd, kettonum):
        self.table      = 'n_uma_race'
        self.cols       = HorseInfoReference.__cols
        if fromymd is None:
            self.conditions = "datakubun='7' AND concat(year, monthday) <= '%s' AND kettonum='%s'" % (id[0] + id[1], kettonum) 
        else:
            self.conditions = "datakubun='7' AND concat(year, monthday) <= '%s' AND concat(year, monthday) > '%s' AND kettonum='%s'" % (id[0] + id[1], fromymd, kettonum) 
        self.order      = 'year ASC, monthday ASC, jyocd ASC, nichiji ASC, racenum ASC'
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class RaceInfoReference:
    __cols = 'kyori, trackcd, honsyokin1, honsyokin2, honsyokin3, honsyokin4, honsyokin5, honsyokin6, honsyokin7, fukasyokin1, fukasyokin2, fukasyokin3, fukasyokin4, fukasyokin5'

    def __init__(self, id):
        self.table      = 'n_race'
        self.cols       = RaceInfoReference.__cols
        self.conditions = "datakubun='7' AND " + IDFilter.generate_phrase(id)
        self.order      = 'year ASC, monthday ASC, jyocd ASC, nichiji ASC, racenum ASC'
        self.limit      = ''

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class IsExistsStatisticsReference:
    __cols =  '1'

    def __init__(self, id):
        self.table      = tablename
        self.cols       = IsExistsStatisticsReference.__cols
        self.conditions = IDFilter.generate_phrase(id)
        self.order      = ''
        self.limit      = ''

class LatestStatisticsReference:
    __cols =  '*'

    def __init__(self, kettonum):
        self.table      = tablename
        self.cols       = LatestStatisticsReference.__cols
        self.conditions = "kettonum='%s'" % (kettonum,)
        self.order      = 'year DESC, monthday DESC, jyocd DESC, nichiji DESC, racenum DESC'
        self.limit      = '1'

    @classmethod
    def index(self, colname):
        return self.__cols.strip().split(', ').index(colname)

class IDReader:
    @classmethod
    def load_data(self, fromyear, toyear, connection):
        with connection.cursor('id_cursor') as cur:
            query = SelectPhrase.generate(IDListReference(fromyear, toyear))
            cur.execute(query)
            id_list  = cur.fetchall()

        return id_list

def load_kettonum_list(id, everydb):
    with everydb.cursor('everydb_cur') as everydb_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(kettonumReference(id))
        everydb_cur.execute(query)

        kettonum_list = []

        while True:
            row = everydb_cur.fetchone()
            if row == None:
                break
            if row[kettonumReference.index('ijyocd')] != '0':
                continue

            kettonum_list.append( row[kettonumReference.index('kettonum')] )

        return kettonum_list

def is_exists_statistics(id, uma_processed):
    with uma_processed.cursor('uma_processed_cur') as up_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(IsExistsStatisticsReference(id))
        up_cur.execute(query)
        row = up_cur.fetchone()

    return row

def load_latest_statistics(kettonum, uma_processed):
    with uma_processed.cursor('uma_processed_cur') as up_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(LatestStatisticsReference(kettonum))
        up_cur.execute(query)
        row = up_cur.fetchone()

    return row

def load_past_uma_race_list(id, fromymd, kettonum, everydb):
    with everydb.cursor('everydb_cur') as everydb_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(HorseInfoReference(id, fromymd, kettonum))
        everydb_cur.execute(query)

        id_list = []
        kakuteijyuni_list = []
        kyakusitukubun_list = []

        while True:
            row = everydb_cur.fetchone()
            if row == None:
                break
            if row[HorseInfoReference.index('ijyocd')] != '0':
                continue

            id_list.append(( row[HorseInfoReference.index('year')],
                             row[HorseInfoReference.index('monthday')],
                             row[HorseInfoReference.index('jyocd')],
                             row[HorseInfoReference.index('kaiji')],
                             row[HorseInfoReference.index('nichiji')],
                             row[HorseInfoReference.index('racenum')]))

            kakuteijyuni_list.append( row[HorseInfoReference.index('kakuteijyuni')] )
            kyakusitukubun_list.append( row[HorseInfoReference.index('kyakusitukubun')] )

        return id_list, kakuteijyuni_list, kyakusitukubun_list

def load_race_info(id, everydb):
    with everydb.cursor('everydb_cur') as everydb_cur:
        # Get race specific uma info from n_race_uma
        query = SelectPhrase.generate(RaceInfoReference(id))
        everydb_cur.execute(query)
        row = everydb_cur.fetchone()
        if row == None:
            raise RuntimeError("Unexpected data shortage of raceinfo")
        return row

def save_statistics(id, kettonum, statistics, connection):
    with connection.cursor() as cur:
        query = InsertPhrase.generate(id, kettonum, statistics)
        cur.execute(query)
    connection.commit()

class StatisticsUpdator:
    def __init__(self):
        try:
            self.connection_raw  = psycopg2.connect(os.environ.get('DATABASE_URL_SRC'))
        except:
            print('psycopg2: opening connection 01 faied')
            sys.exit(0)

        try:
            self.connection_processed = psycopg2.connect(os.environ.get('DB_UMA_PROCESSED'))
        except:
            print('psycopg2: opening connection 02 faied')
            sys.exit(0)

    def __del__(self):
        self.connection_raw.close()
        self.connection_processed.close()

    def process(self, fromyearmonthday, toyearmonthday):
        id_list = IDReader.load_data(fromyearmonthday, toyearmonthday, self.connection_raw)

        for id in tqdm(id_list, desc='Gathering race data'):
            print('\nprocessing id: %s%s%s%s%s%s' % id)
            #print('\nprocessing id: %s%s%s%s%s%s' % id)

            try:
                kettonum_list = load_kettonum_list(id, self.connection_raw)
            except RuntimeError as e:
                print(e)
                continue

            for kettonum in kettonum_list:
                print('processing ketto: %s\n' % kettonum, end='\033[1A\r', flush=True)
                statistics_row = load_latest_statistics(kettonum, self.connection_processed)
                if not statistics_row is None:
                    latest_statistics = gen_initial_statistics()
                    for key, i in zip(latest_statistics.keys(), range(len(latest_statistics))):
                        latest_statistics[key] = statistics_row[7 + i]
                    latestymd = statistics_row[0] + statistics_row[1]
                else:
                    latest_statistics = gen_initial_statistics()
                    latestymd = None

                past_id_list, kakuteijyuni_list, kyakusitukubun_list = load_past_uma_race_list(id, latestymd, kettonum, self.connection_raw)
                for pastid, kakuteijyuni, kyakusitukubun in zip(past_id_list, kakuteijyuni_list, kyakusitukubun_list):
                    try:
                        race_info = load_race_info(pastid, self.connection_raw)
                    except RuntimeError as e:
                        print(e)
                        exit()

                    try:
                        update_statistics(latest_statistics, race_info, kakuteijyuni, kyakusitukubun)
                    except RuntimeError as e:
                        print(e)
                        continue

                try:
                    save_statistics(id, kettonum, latest_statistics, self.connection_processed)
                except RuntimeError as e:
                    print(e)
                    exit()

            print('', end='\033[2A\r', flush=True)

        print('\n\n\n\n')

if __name__ == "__main__":
    updator = StatisticsUpdator()
    updator.process('19970320', '20200000')
    #updator.process('19900000', '20200000')
    #updator.process('19990000', '20100000')
    #updator.process('20100000', '20200000')

