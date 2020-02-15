import tensorflow as tf
a = tf.constant([2.0, 3.0])
with tf.Session() as sess:
  print(sess.run(a))
