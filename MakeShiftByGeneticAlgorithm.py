######################################################################################## import
import random
from decimal import *
import time
import datetime
######################################################################################## setting
################################################ ユーザ指定項目
# 平日勤務体制
WEEKDAY_SHIFT_PATTERN = ['A','A','A','C', 'B','X','X','X']
# 土日祝日勤務体制
HOLIDAY_SHIFT_PATTERN = ['A','B','X','X', 'X','X','X','X']
# 勤務時間
WORK_TIME             = {'A':8, 'B':15, 'C':8, 'X':0}
# 休日・夜勤設定
REST  = 'X'
NIGHT = 'B'
# 希望休 # 左上から１人目
# OFF_DAY = [
#     [1,2,3,],[4,5,6,],[7,8,9,],
#     [10,11,12,],[13,14,15,],[16,17,18,],
#     [19,20,21,],[22,23,24,],
# ] 
# ３人目の希望日は７、８、９日となる
# ４人目の希望日は１０、１１、１２日となる
OFF_DAY = [
    [1,2,3,],[4,5,6,],[7,8,9,],
    [10,11,12,],[13,14,15,],[16,17,18,],
    [19,20,21,],[22,23,24,],
]
# 土日祝日
WHEN_IS_HOLIDAY = [1,2,3,4,5,6, 11,12, 18,19, 25,26]
# 作成する日数
DAY_LENGTH      = 31
# 禁止連続日数  N日まで
MAX_CONSECUTIVE_WORK = 5
################################################ ユーザ指定項目　ここまで
# 選択するエリート数
ELITE_LENGTH     = 20
# シフト数
MAX_SHIFT_LENDTH = 100
# 繰り返し世代数（制限ありの場合）
MAX_GENERATION   = 100000
# 変異確率
INDIVIDUAL_MUTATION = 0.5
# 日別変異確率
DAY_MUTATION = 0.08
# 諦め （設定必須）
MAX_CONTINUE = 5000
######################################################################################## class
class GenomShift:
    ### length_shift
    # [0,0,0,0,0] 1日目
    # ...
    # ...
    # [0,0,0,0,0] N日目
    length_shift = None
    
    ### width_shift
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 1人目
    # ...
    # ...
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] N人目
    width_shift = None
    
    ### evaluation = integer型 数値が低いほど高評価
    evaluation = 0
    
    ### 不良箇所のインデックスを格納　width_shift型
    error_line = []
    
    def __init__(self, length_shift, evaluation):
        self.length_shift = length_shift
        self.evaluation   = evaluation
        width_shift = [[ l[i] for l in self.length_shift ] for i in range(len(self.length_shift[0])) ]
        self.width_shift = width_shift
        
    # GET #
    def getLengthShift(self):
        return self.length_shift    
    def getWidthShift(self):
        return self.width_shift
    def getEvaluation(self):
        return self.evaluation
    def getErrorLine(self):
        return self.error_line
    
    # SET #
    def setLengthShift(self, length_shift):
        self.length_shift = length_shift
        width_shift = [[ l[i] for l in self.length_shift ] for i in range(len(self.length_shift[0])) ]
        self.width_shift  = width_shift
    def setWidthShift(self, width_shift):
        self.width_shift = width_shift
        length_shift = [[ l[i] for l in self.width_shift ] for i in range(len(self.width_shift[0])) ]
        self.length_shift = length_shift
    def setEvaluation(self, evaluation):
        self.evaluation = evaluation
    def setErrorLine(self, error_line):
        self.error_line = error_line

class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'
######################################################################################## def
### 命名ルール ###
# クラス複数 = objects
# クラス単体 = obj
# シフト２次配列時 = shift_data -> shift_data[0] = shift
# シフト１次配列時 = shift -> shift[0] = s
# シフト内容 = s -> s = 'A'
# 簡易変数 = m
#####

# インスタンスを生成する
def create(weekday_shift_pattern, day_length):
    length_shift = []
    for d in range(day_length):
        # 変数省略
        wp = weekday_shift_pattern
        ls = [i for i in random.sample(wp, len(wp))]
        length_shift.append(ls)
    return GenomShift(length_shift, 0)

# エリートを選択する
def select(objects, elite_length):
    ### エリート保存戦略 ###
    # sorted_objects = sorted(objects, reverse=False, key=lambda u: u.evaluation)
    # elite_objects = [sorted_objects.pop(0) for i in range(elite_length)]
    
    ### トーナメント式 ###
    # ランダムに選手を選択し、ソートする
    selected_objects = random.sample(objects, elite_length*3)
    sorted_objects   = sorted(selected_objects, reverse=False, key=lambda u: u.evaluation)
    elite_objects    = [sorted_objects.pop(0) for i in range(elite_length)]
    # elite_objects をランダムに抽出
    elite_objects    = random.sample(elite_objects, len(elite_objects))
    return elite_objects

# 一点交叉
def crossover(red, blue, day_length):
    # cp = cross_point 交叉位置
    cp = random.randint(0, day_length)
    # length_shift を取得
    red_shift  = red.getLengthShift()
    blue_shift = blue.getLengthShift()
    # 交叉開始
    first_shift  = red_shift[:cp] + blue_shift[cp:]
    second_shift = blue_shift[:cp] + red_shift[cp:]
    # 新たにインスタンスを生成し、格納する
    cross_objects = []
    cross_objects.append(GenomShift(first_shift,0))
    cross_objects.append(GenomShift(second_shift,0))
    return cross_objects

# 評価・審査
def evaluate(obj, max_consecutive_work, rest, night):
    # 評価値を格納
    point = 0
    ### N連続勤務 ###
    # 'X' = 休み
    # width_shiftを使用
    # ['A','C','A','A','C','A','C'.......] work_cnt = 7
    # ['A','C','X','A','C','X','C'.......] work_cnt = 1
    # P = 評価値
    P = 1
    for shift in obj.getWidthShift():
        work_cnt = 0
        for s in shift:
            # その日が休みなら、カウンター　＋１
            work_cnt = [0, work_cnt + 1][s != rest]
            if work_cnt > max_consecutive_work:
                point += P
                continue

    ### 夜勤明けに日勤（夜勤後は必ず休み） ###
    # 'B' = 夜勤
    # 夜勤明けに日勤の場合 += 1
    # width_shiftを使用
    # ['B','X','B','A','B','C','X'.......] = 2
    # P = 評価値
    P = 1
    for shift in obj.getWidthShift():
        # 初日をスキップ
        for i in range(1, len(shift)):    
            # 昨晩夜勤である　かつ　今日休み以外の場合
            if shift[i-1] == night and shift[i] != rest:
                point += P
            else: continue
    obj.setEvaluation(point)
    return obj

# 変異
def mutation(objects, individual_mutation, day_mutation):
    # 変数名省略
    im = individual_mutation
    dm = day_mutation
    mutant_objects = []
    for obj in objects:
        # 100分の　im の確率で変異対象とする
        if im > (random.randint(0, 100) / Decimal(100)):
            mutant_shift = []
            for shift in obj.getLengthShift():
                # 100分の　dm の確率でその日を変異対象とする
                if dm > (random.randint(0, 100) / Decimal(100)):
                    shift = random.sample(shift, len(shift))
                    mutant_shift.append(shift)
                else:
                    mutant_shift.append(shift)
            mutant_objects.append(GenomShift(mutant_shift, 0))
        else:
            mutant_objects.append(obj)
    return mutant_objects

# 新たな世代を作成
def create_new_objects(objects, elite_objects, cross_objects):
    sorted_objects = sorted(objects, reverse=True, key=lambda u:u.evaluation)
    # 新世代 = 現世代 - (エリート数 + 交叉数) + エリート + 交叉
    # 100 = 100 - (30 + 60) + 30 + 60
    n = len(elite_objects) + len(cross_objects)
    for i in range(n):
        sorted_objects.pop(0)
    sorted_objects.extend(elite_objects)
    sorted_objects.extend(cross_objects)
    return sorted_objects

# # 希望休複数申請 #
# OFF_DAY = ２次配列
def take_rest(obj, off_day, rest):
    # length_shiftを取得
    shift_data = obj.getLengthShift()
    sd = shift_data
    # 希望日リストからスタッフインデックスとその人の希望日リストを抽出
    for staf_id, rest_days in enumerate(off_day):
        # 希望日リストの内容を抽出
        for r_day in rest_days:
            r_day -= 1
            # 希望日が休みの場合はスキップ
            if sd[r_day][staf_id] == rest: continue
            # その日の中で他に休みの人を探すために、その日の内容を抽出
            for other_id, other_day in enumerate(sd[r_day]):
                # 希望日を申請している人はスキップ
                if other_id == staf_id: continue
                # 他の人が休みの場合
                if other_day == rest and r_day+1 not in off_day[other_id]:
                    sd[r_day][staf_id], sd[r_day][other_id] = sd[r_day][other_id], sd[r_day][staf_id]
                    break
    obj.setLengthShift(shift_data)
    return obj
    
# 1人の勤務時間の合計を返す
def count_work_time(shift, work_time):
    wt = [ work_time[s] for s in shift ]
    return sum(wt)

# 勤務時間を評価
def evaluate_work_time(obj, work_time, work_avg):
    ### 勤務時間を評価 ###
    # 評価値
    P     = 1
    point = 0
    
    for shift in obj.getWidthShift():
        # １人の勤務時間を取得
        cwt = count_work_time(shift, work_time)
        # 規定の範囲外なら、(絶対値(勤務時間 - 平均時間 + 閾値)　/ 100)
        point += Decimal(abs(cwt - round(work_avg,1))) / Decimal(100)
    m = obj.getEvaluation()
    obj.setEvaluation(m + point)
    return obj
    
# 土日祝日のシフトを書き込み　オブジェクトを返す
def add_holiday_shift(obj, holiday_shift_pattern, when_is_holiday):
    # 変数省略
    hsp = holiday_shift_pattern
    wih = when_is_holiday
    shift_data = obj.getLengthShift()
    for wh in wih:
        shift_data[ wh - 1 ] = random.sample(hsp, len(hsp))
    obj.setLengthShift(shift_data)
    return obj
############################################## 作成中
# 不良箇所を特定 勤務時間を判定
def whereis_error_work_time(obj, work_time, work_avg):
    min_max = 5
    error_line = obj.getErrorLine()
    for i, shift in enumerate(obj.getWidthShift()):
        tal = 0
        for s in shift:
            tal += work_time[s]
        if abs(tal - work_avg) > min_max:
            if i not in error_line:
                error_line.append(i)
    obj.setErrorLine(error_line)
    return obj
    
# 不良箇所を特定 夜勤明けを判定
def whereis_error_night_work(obj, night, rest):
    error_line = obj.getErrorLine()
    for e, shift in enumerate(obj.getWidthShift()):
        for i in range(1, len(shift)):
            if shift[i-1] == night and shift[i] != rest:
                if e not in error_line:
                    error_line.append(e)
    obj.setErrorLine(error_line)
    return obj 
# 不良箇所を特定 連続勤務を判定
def whereis_error_consentive_work():
    pass

# 不良箇所に色付け
def add_error_line_color(error_line, shift_data, color):
    color_shift_data = []
    for i, shift in enumerate(shift_data):
        if i in error_line:
            color_shift = [ color + s + Color.END for s in shift ]
        else:
            color_shift = [ s for s in shift ]
        color_shift_data.append(color_shift)
    return color_shift_data
############################################## 作成中
######################################################################################## main
if __name__=='__main__':
    # 処理時間を測定
    t1 = time.time()
    dt1 = datetime.datetime.now()
    # ループ制御変数
    last_min = None
    same_cnt = 0
    # 初期状態
    objects = ( create(WEEKDAY_SHIFT_PATTERN, DAY_LENGTH) for i in range(MAX_SHIFT_LENDTH) )
    objects = [ add_holiday_shift(obj, HOLIDAY_SHIFT_PATTERN, WHEN_IS_HOLIDAY) for obj in objects ]
    # 平均勤務時間を取得
    m    = [ count_work_time(shift, WORK_TIME) for shift in objects[0].getWidthShift() ]
    WORK_AVG = sum(m) / len(m)
    # 評価
    objects = ( evaluate(obj, MAX_CONSECUTIVE_WORK, REST, NIGHT) for obj in objects )
    # 勤務時間を評価
    objects = [ evaluate_work_time(obj, WORK_TIME, WORK_AVG) for obj in objects ]
    
    # 世代交代開始 ############################################################
    
    # 世代交代（制限あり）
    for count in range(1, MAX_GENERATION + 1):
        # エリート選択
        elite_objects = select(objects, ELITE_LENGTH)
        # 交叉
        cross_objects = []
        for i in range(ELITE_LENGTH):
            m = crossover(elite_objects[i-1], elite_objects[i], DAY_LENGTH)
            cross_objects.extend(m)
        # 世代交代
        new_objects = create_new_objects(objects, elite_objects, cross_objects)
        # 変異
        new_objects = mutation(new_objects, INDIVIDUAL_MUTATION, DAY_MUTATION)
        # 希望休をとる
        new_objects = ( take_rest(obj, OFF_DAY, REST) for obj in new_objects )
        # 評価
        new_objects = ( evaluate(obj, MAX_CONSECUTIVE_WORK, REST, NIGHT) for obj in new_objects )
        # 勤務時間を評価
        new_objects = [ evaluate_work_time(obj, WORK_TIME, WORK_AVG) for obj in new_objects ]
        # 現行と新世代を入れ替え
        objects = new_objects
        
        # 進化結果
        fits = [i.getEvaluation() for i in objects]
        min_ = min(fits)
        max_ = max(fits)
        avg_ = sum(fits) / Decimal(len(fits))
        ### 最小値を比較 ###
        if last_min == None: last_min = min_
        # 最小評価値が０になったら終了
        if min_ <= 0: break
        # 最小評価値が N 世代変化がない場合終了
        N = MAX_CONTINUE
        if same_cnt >= N: break
        # 現世代と前世代の最小評価値が同じならカウンター　＋１
        if last_min == min_:
            same_cnt += 1
        # それ以外は前世の変数を更新、カウンター　０
        else:
            same_cnt = 0
            last_min = min_
        # 中間結果
        if count % 1000 == 0 or count == 1:
            print("-----第{}世代の結果-----".format(count))
            print("  Min:{}".format(min_))
            print("  Max:{}".format(max_))
            print("  Avg:{}".format(avg_))
            print('  Cnt:{}'.format(same_cnt))
    # 世代交代終了 ############################################################

    # 最優秀シフトを選択
    sorted_objects = sorted(objects, reverse=False, key=lambda u: u.evaluation)
    best_obj       = sorted_objects[0]
    # エラー箇所を取得
    best_obj       = whereis_error_work_time(best_obj, WORK_TIME, WORK_AVG)
    best_obj       = whereis_error_night_work(best_obj, NIGHT, REST)
    # 日付を作成
    days = [ str(i).rjust(2) for i in range(1,DAY_LENGTH+1) ]
    # 設定値を表示
    print('\n=== 設定 =================================')
    print('  日数　　　　　: {}'.format(DAY_LENGTH))
    print('  勤務時間　　　: {}'.format(WORK_TIME))
    print('  平日シフト　　: {}'.format(WEEKDAY_SHIFT_PATTERN))
    print('  土日祝日シフト: {}'.format(HOLIDAY_SHIFT_PATTERN))
    print('  土日祝日　　　: {}'.format(WHEN_IS_HOLIDAY))
    for e, i in enumerate(OFF_DAY):
        print('  希望休{}人目　: {}'.format(str(e+1).rjust(2), i))
    print('  連勤　　　　　: {}日まで'.format(MAX_CONSECUTIVE_WORK))
    print('  {} = 休み'.format(REST))
    print('  {} = 夜勤'.format(NIGHT))
    print('  夜勤明けは休み')
    print('===========================================')
    # 最優秀シフトの情報を表示
    print('-----第{}世代の結果-----'.format(count))
    print('  減点：{0}  平均勤務時間：{1} '.format(best_obj.getEvaluation(), round(WORK_AVG,1) ))
    if best_obj.getErrorLine() != None:
        for i in best_obj.getErrorLine():
            print('  要修正：{}人目'.format(i+1))
    print('-------------------------------------------'*4)
    # 日付を表示
    print('{} ['.format(str('-').rjust(2)), end='')
    for d in days[:-1]:
        print('\'{}\''.format(d), end=', ')
    print('\'{}\''.format(days[-1]), end='] Avg: '+ str(round(WORK_AVG,1)) +'\n')
    # シフトを表示
    for i, shift in enumerate(best_obj.getWidthShift()):
        ajust_shift = [ s.rjust(2) for s in shift] 
        print('{2} {0} Tal: {1}'.format(ajust_shift, count_work_time(shift, WORK_TIME), str(i+1).rjust(2)))
    print('-------------------------------------------'*4)
    # 日付を表示（色付き）
    color_days = [ Color.RED + d + Color.END if int(d) in WHEN_IS_HOLIDAY else d for d in days ]
    print('{} ['.format(str('-').rjust(2)), end='')
    for d in color_days[:-1]:
        print('\'{}\''.format(d), end=', ')
    print('\'{}\''.format(color_days[-1]), end='] Avg: '+ str(round(WORK_AVG,1)) +'\n')
    # シフト表示（色付き）
    error_line = best_obj.getErrorLine()
    shift_data = best_obj.getWidthShift()
    ajust_shift = [[ s.rjust(2) for s in shift ] for shift in shift_data]
    color_shift_data = [[ Color.YELLOW + s + Color.END for s in shift ] if i in error_line else [ s for s in shift ] for i, shift in enumerate(ajust_shift) ]
    for i, shift in enumerate(color_shift_data):
        print('{} ['.format(str(i+1).rjust(2)), end='')
        for s in shift[:-1]:
            print('\'{}\''.format(s), end=', ')
        print('\'{0}\'] Tal: {1}'.format(shift[-1], str(count_work_time(shift_data[i], WORK_TIME))))
    print('-------------------------------------------'*4)

    # 日付を表示（CSV）
    print(*days[:-1], sep=',', end=',' + days[-1] + ',' + str(round(WORK_AVG,1)))
    print()
    # シフト表示（CSV）
    for shift in best_obj.getWidthShift():
        ajust_shift = [s.rjust(2) for s in shift]
        print(*ajust_shift, sep=',', end=',')
        print('{}'.format(count_work_time(shift, WORK_TIME)))
    print('-------------------------------------------'*4)
    # 処理後の時刻を表示
    t2 = time.time()
    tm = t2-t1
    print('  処理時間：{}s'.format(round(tm, 2)))
    dt2 = datetime.datetime.now()
    date = dt2-dt1
    print('  処理時間：{}'.format(str(date)[:-7]))

######################################################################################## test