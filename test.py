#import tensorflow as tf
#a = tf.constant([2.0, 3.0])
#with tf.compat.v1.Session() as sess:
#  print(sess.run(a))
#g=tf.Graph()
#with g.as_default():
#    v_1 = tf.constant([1, 2, 3, 4])
#    v_2 = tf.constant([2, 3, 4, 5])
#    v_add = tf.add(v_1, v_2)
#    sess=tf.compat.v1.Session(graph=g)
#    print(sess.run(v_add))

#coding:utf-8
import tensorflow as tf

#1. 定义变量及滑动平均数
#定义一个32位浮点变量，初始值为0.0；这个代码就是不断更新w1参数，优化w1参数，滑动平均做了个w1的影子
w1 = tf.Variable(0, dtype=tf.float32)
#定义num_updates（NN的迭代轮数），初始值为0，这个参数不训练
global_step = tf.Variable(0, trainable=False)
#实例化滑动平均数，给衰减率设为0.99，当前轮数global_step
MOVING_AVERAGE_DECAY = 0.99
ema = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
#ema.apply后的括号里是更新列表，每次运行sess.run(ema_op)时，对更新列表中的元素求滑动平均值。
#在实际应用中会使用tf.trainable_variables()自动将所有待训练的参数汇总成列表
#ema_op = ema.apply([])，apply当一个函数的参数存在于一个元组或者一个字典中时，用来间接的调用这个函数，并将元组或字典中的参数按照顺序传递给参数。
ema_op = ema.apply(tf.compat.v1.trainable_variables())   #对所有待优化的参数求滑动平均

#2. 查看不同迭代中变量取值的变化。
with tf.compat.v1.Session() as sess:
    init_op = tf.compat.v1.global_variables_initializer()
    sess.run(init_op)
    #用ema.average(w1)获取w1滑动平均值（要运行多个节点，作为列表中的元素列出，卸载sess.run中）
    #打印出当前参数w1和w1滑动平均值
    print(sess.run([w1, ema.average(w1)]))   #ema.average(参数名)    #查看某参数的滑动平均值
#    with tf.control_dependencies([train_step, ema_op]):
#    train_op = tf.no_op(name="train")
    
    #参数w1的值设为1
    sess.run(tf.assign(w1, 1))
    sess.run(ema_op)
    
    #更新step和w1的值，模拟出100轮迭代后，参数w1变为10
    sess.run(tf.assign(global_step, 100))
    sess.run(tf.assign(w1, 1))
    sess.run(ema_op)
    print(sess.run([w1, ema.average(w1)]))
    
    #每次sess.run会更新一次w1的滑动平均值
    sess.run(ema_op)
    print(sess.run([w1, ema.average(w1)]))
    
    sess.run(ema_op)
    print(sess.run([w1, ema.average(w1)]))
