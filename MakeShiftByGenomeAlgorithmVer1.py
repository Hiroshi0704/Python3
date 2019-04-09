############################################ import
import random
from decimal import *
############################################ class

class GenomShift:

	length_shift = None
	### length_shift
	# [0,0,0,0,0] day 1
	# ...
	# ...
	# [0,0,0,0,0] day last

	width_shift = None
	### width_shift
	# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] staff 1
	# ...
	# ...
	# [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] staff last

	evaluation = None
	### evaluation = integer 数値が低いほど高評価
	
	def __init__(self, length_shift, evaluation):
		self.length_shift = length_shift
		self.evaluation = evaluation
		# width_shiftへ変換
		width_shift = []
		for i in range(len(self.length_shift[0])):
			m = []
			for l in self.length_shift:
				m.append(l[i])
			width_shift.append(m) 
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
		# width_shiftへ変換
		width_shift = []
		for i in range(len(self.length_shift[0])):
			m = []
			for l in self.length_shift:
				m.append(l[i])
			width_shift.append(m) 
		self.width_shift = width_shift
	
	def setWidthShift(self, width_shift):
		self.width_shift = width_shift
		# length_shiftへ変換
		length_shift = []
		for i in range(len(self.width_shift[0])):
			m = []
			for w in self.width_shift:
				m.append(w[i])
			length_shift.append(m)
		self.length_shift = length_shift

	def setEvaluation(self, evaluation):
		self.evaluation = evaluation

############################################ def
### 命名ルール ###
# クラス複数 = objects
# クラス単体 = obj
# シフト２次配列時 = shift_data -> shift_data[0] = shift
# シフト１次配列時 = shift -> shift[0] = s
# シフト内容 = s -> s = 'A'
# 簡易変数 = m
#####

# クラスインスタンスを生成する
def create(shift_pattern, day_length):

	length_shift = []
	for d in range(day_length):
		sp = shift_pattern
		ls = [i for i in random.sample(sp, len(sp))]
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

	### 絶対事項 ###
	・1人１日希望休の申請
	・平均的な勤務時間

	#### 上記整理 ####
	# 7連続勤務 #
	'X' = 休み
	length_shiftを使用
	['A','C','A','A','C','A','C'.......] work_cnt = 7
	['A','C','X','A','C','X','C'.......] work_cnt = 1

	# 夜勤明けに日勤 #
	夜勤明けに日勤の場合 = True
	length_shiftを使用
	['B','X','B','A','B','C','X'.......] true_cnt = 2

	# 1人１日希望休の申請 #
	８人の場合、８人の希望休をリストへ格納
	[1, 4, 6, 8, 9, 10, 26, 15] ３人目の希望休は６日目
	width_lengthを使用
	希望休ではない場合は休みの人と入れ替える

	# 平均的な勤務時間 #
	length_shiftを使用
	勤務時間を計算し	
	'''
	pass
	
### 命名ルール ###
# クラス複数 = objects
# クラス単体 = obj
# シフト２次配列時 = shift_data -> shift_data[0] = shift
# シフト１次配列時 = shift -> shift[0] = s
# シフト内容 = s -> s = 'A'
# 簡易変数 = m
#####

# 変異
def mutation(objects, individual_mutation, day_mutation, weekday_shift_pattern):
	# 変数名省略
	im = individual_mutation
	dm = day_mutation
	wp = weekday_shift_pattern
	
	new_objects = []
	for obj in objects:
		if im > (random.randint(0, 100) / Decimal(100)):
			mutant_shift = []
			for shift in obj.getLengthShift():
				if dm > (random.randint(0, 100) / Decimal(100)):
					shift = random.sample(wp, len(wp))
					mutant_shift.append(shift)
				else:
					mutant_shift.append(shift)
			new_objects.append(GenomShift(mutant_shift, 0))
		else:
			new_objects.append(obj)
	return new_objects

# 新たな世代を作成
def create_new_objects(objects, elite_objects, cross_objects):
	new_objects = sorted(objects, reverse=True, key=lambda u:u.evaluation)
	
	n = len(elite_objects) + len(cross_objects)
	for i in range(n):
		new_objects.pop(0)
	new_objects.extend(elite_objects)
	new_objects.extend(cross_objects)
	return new_objects


############################################ setting
WEEKDAY_SHIFT_PATTERN = ['A','A','A','B','B','C','X','X']

DAY_LENGTH = 28
ELITE_LENGTH = 20

MAX_SHIFT_LENDTH = 100
MAX_GENERATION = 40

INDIVIDUAL_MUTATION = 0.1
DAY_MUTATION = 0.1
############################################ main

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
	
	for i in range(MAX_SHIFT_LENDTH):
		m = create(WEEKDAY_SHIFT_PATTERN, DAY_LENGTH)
		objects.append(m)
	
	print('\n========== object[0] ==========')
	for i in objects[0].getWidthShift():
		print(i)
		
	elite_objects = select(objects, ELITE_LENGTH)
	
	print('\n========== elite[0] ==========')
	for i in elite_objects[0].getWidthShift():
		print(i)
	
	for i in range(len(elite_objects)):
		m = crossover(elite_objects[i-1], elite_objects[i], DAY_LENGTH)
		cross_objects.extend(m)
	
	print('\n========== cross[0] ==========')
	for i in cross_objects[0].getWidthShift():
		print(i)
		
	objects = mutation(objects, INDIVIDUAL_MUTATION, DAY_MUTATION, WEEKDAY_SHIFT_PATTERN)
	
	print('\n========== mutant[0] ==========')
	for i in objects[0].getWidthShift():
		print(i)
	
	new_objects = create_new_objects(objects, elite_objects, cross_objects)
	

############################################ test
















