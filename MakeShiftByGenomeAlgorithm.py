######################################################################################## import
import random
from decimal import *
######################################################################################## class

class GenomShift:

	### length_shift
	# [0,0,0,0,0] day 1
	# ...
	# ...
	# [0,0,0,0,0] day last
	length_shift = None

	### width_shift
	# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] staff 1
	# ...
	# ...
	# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] staff last
	width_shift = None

	### evaluation = integer型 数値が低いほど高評価
	evaluation = 0
	
	def __init__(self, length_shift, evaluation):
		self.length_shift = length_shift
		self.evaluation = evaluation
		# width_shiftへ変換
		'''
		width_shift = []
		for i in range(len(self.length_shift[0])):
			m = []
			for l in self.length_shift:
				m.append(l[i])
			m = [ l[i] for l in self.length_shift ]
			width_shift.append(m)
		'''
		# 上記の内包表記
		width_shift = [[ l[i] for l in self.length_shift ] for i in range(len(self.length_shift[0])) ]

		self.width_shift = width_shift


	# GET #
	def getLengthShift(self):
		return self.length_shift
	
	def getWidthShift(self):
		return self.width_shift
	
	def getEvaluation(self):
		return self.evaluation
	
	# SET #
	def setLengthShift(self, length_shift):
		self.length_shift = length_shift
		width_shift = [[ l[i] for l in self.length_shift ] for i in range(len(self.length_shift[0])) ]
		self.width_shift = width_shift
	
	def setWidthShift(self, width_shift):
		self.width_shift = width_shift
		# length_shiftへ変換
		'''
		length_shift = []
		for i in range(len(self.width_shift[0])):
			m = []
			for w in self.width_shift:
				m.append(w[i])
			length_shift.append(m)
		'''
		length_shift = [[ w[i] for w in self.width_shift ] for i in range(len(self.width_shift[0])) ]
		self.length_shift = length_shift

	def setEvaluation(self, evaluation):
		self.evaluation = evaluation

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
	sorted_objects = sorted(objects, reverse=False, key=lambda u: u.evaluation)
	elite_objects = [sorted_objects.pop(0) for i in range(elite_length)]
	return elite_objects

# 一点交叉
def crossover(red, blue, day_length):
	# cp = cross_point 交叉位置
	cp = random.randint(0, day_length)
	# length_shift を取得
	red_shift = red.getLengthShift()
	blue_shift = blue.getLengthShift()
	
	# 交叉開始
	first_shift = red_shift[:cp] + blue_shift[cp:]
	second_shift = blue_shift[:cp] + red_shift[cp:]
	
	# 新たにインスタンスを生成し、格納する
	cross_objects = []
	cross_objects.append(GenomShift(first_shift,0))
	cross_objects.append(GenomShift(second_shift,0))
	return cross_objects

# 評価・審査
def evaluate(obj):
	'''
	### 禁止事項 ###
	・7連続勤務
	・夜勤明けに日勤（夜勤後は必ず休み）

	#### 上記整理 ####
	# 7連続勤務 #
	'X' = 休み
	width_shiftを使用
	['A','C','A','A','C','A','C'.......] work_cnt = 7
	['A','C','X','A','C','X','C'.......] work_cnt = 1

	# 夜勤明けに日勤 #
	'B' = 夜勤
	夜勤明けに日勤の場合 += 2
	width_shiftを使用
	['B','X','B','A','B','C','X'.......] += 4
	'''

	obj.setEvaluation(0)
	point = 0

	### ７連続勤務判定 ### 
	# 評価値：３
	P = 3
	for shift in obj.getWidthShift():
		work_cnt = 0
		for s in shift:
			if work_cnt >= 7:
				work_cnt = 0
				point += P
				continue

			if s == REST:
				work_cnt = 0
			else:
				work_cnt += 1

	### 夜勤明けに日勤（夜勤後は必ず休み） ###
	# 評価値：２
	P = 2
	for shift in obj.getWidthShift():
		for i in range(len(shift)):
			# 初日をスキップ
			if i == 0: continue
			# 昨晩夜勤だった場合　かつ　今日休み以外の場合
			if shift[i-1] == NIGHT and shift[i] != REST:
				point += P
			else: continue

	obj.setEvaluation(point)
	return obj

# 変異
def mutation(objects, individual_mutation, day_mutation, weekday_shift_pattern):
	# 変数名省略
	im = individual_mutation
	dm = day_mutation
	wp = weekday_shift_pattern
	
	mutant_objects = []
	for obj in objects:
		if im > (random.randint(0, 100) / Decimal(100)):
			mutant_shift = []
			for shift in obj.getLengthShift():
				if dm > (random.randint(0, 100) / Decimal(100)):
					shift = random.sample(wp, len(wp))
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
	
	n = len(elite_objects) + len(cross_objects)
	for i in range(n):
		sorted_objects.pop(0)
	sorted_objects.extend(elite_objects)
	sorted_objects.extend(cross_objects)
	return sorted_objects


'''
# 1人１日希望休の申請 #
８人の場合、８人の希望休をリストへ格納
[1, 4, 6, 8, 9, 10, 26, 15] ３人目の希望休は６日目となる
length_shiftを使用
希望休ではない場合は休みの人と入れ替える
'''
def take_rest(obj, off_day):

	shift = obj.getLengthShift()
	for staff, day in enumerate(off_day):
		if shift[day - 1][staff] != REST:
			for i, s in enumerate(shift[day - 1]):
				if i == staff: continue
				if s == REST:
					shift[day - 1][staff], shift[day - 1][i] = shift[day - 1][i], shift[day - 1][staff]
	
	obj.setLengthShift(shift)
	return obj

######################################################################################## setting
WEEKDAY_SHIFT_PATTERN = ['A','A','A','B','C','X','X','X']
REST = 'X'
NIGHT = 'B'

OFF_DAY = [1,2,3,4,5,6,7,8]

DAY_LENGTH = 28
ELITE_LENGTH = 20

MAX_SHIFT_LENDTH = 100
MAX_GENERATION = 120

INDIVIDUAL_MUTATION = 0.1
DAY_MUTATION = 0.1
######################################################################################## main

### 命名ルール ###
# クラス複数 = objects
# クラス単体 = obj
# シフト２次配列時 = shift_data -> shift_data[0] = shift
# シフト１次配列時 = shift -> shift[0] = s
# シフト内容 = s -> s = 'A'
# 簡易変数 = m
#####

if __name__=='__main__':
	objects = []
	elite_objects = []
	cross_objects = []
	
	# 初期状態
	objects = [ create(WEEKDAY_SHIFT_PATTERN, DAY_LENGTH) for i in range(MAX_SHIFT_LENDTH) ]
	
	# 世代交代開始 ############################################ for
	for count in range(1, MAX_GENERATION + 1):
		
		# 評価
		objects = [ evaluate(obj) for obj in objects ]
		
		# 希望休をとる
		objects = [ take_rest(obj, OFF_DAY) for obj in objects ]

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
		new_objects = mutation(new_objects, INDIVIDUAL_MUTATION, DAY_MUTATION, WEEKDAY_SHIFT_PATTERN)

		# 進化結果を表示
		fits = [i.getEvaluation() for i in objects]

		min_ = min(fits)
		max_ = max(fits)
		avg_ = sum(fits) / Decimal(len(fits))

		print ("-----第{}世代の結果-----".format(count))
		print ("  Min:{}".format(min_))
		print ("  Max:{}".format(max_))
		print ("  Avg:{}".format(avg_))

		# 現行と新世代を入れ替え
		objects = new_objects

		# 終了条件
		if min_ <= 0: break
	
	# 世代交代終了 ############################################ endfor

	print('\n=== 設定 ========')
	print('日数：{}'.format(DAY_LENGTH))
	print('シフトタイプ：{}'.format(WEEKDAY_SHIFT_PATTERN))
	print('希望休：{}'.format(OFF_DAY))
	print('{} = 休み'.format(REST))
	print('{} = 夜勤'.format(NIGHT))
	print('7連勤禁止')
	print('夜勤明けは必ず休み')
	print('==================')
	print('最適化したシフト')
	days = [str(i).rjust(2) for i in range(1,DAY_LENGTH+1)]
	elite_shift = [[ s.rjust(2) for s in shift] for shift in elite_objects[0].getWidthShift() ]
	print('====='*35)
	print(days)
	for i in elite_shift:
		print(i)
	print('====='*35)

######################################################################################## test