import tensorflow as tf

from model import Model

from preprocess import *

SEED = 24

print('Loading dataset...')
X_train, Y_train, X_val, Y_val, X_test, Y_test = load_CIFAR(SEED)

X_train = X_train[0:1000,:,:,:]
Y_train = Y_train[0:1000,:,:,:]

X_val = X_val[0:100,:,:,:]
Y_val = Y_val[0:100,:,:,:]

X_test = X_test[0:100,:,:,:]
Y_test = Y_test[0:100,:,:,:]

print('Train:')
print('X_train:', X_train.shape)
print('Y_train:', Y_train.shape)

print('Validation:')
print('X_val:', X_val.shape)
print('Y_val:', Y_val.shape)

print('Test:')
print('X_test:', X_test.shape)
print('Y_test:', Y_test.shape)

save_gray_images(X_train[0:10,:,:,:], filename="images/train_{}/before_gray.png")
save_lab_images(Y_train[0:20,:,:,:], filename="images/train_{}/before_color.png")

save_gray_images(X_val[0:10,:,:,:], filename="images/val_{}/before_gray.png")
save_lab_images(Y_val[0:20,:,:,:], filename="images/val_{}/before_color.png")

save_gray_images(X_test[0:100,:,:,:], filename="images/test/gray_{}.png")
save_lab_images(Y_test[0:100,:,:,:], filename="images/test/original_{}.png")

np.random.seed(SEED)
tf.random.set_seed(SEED)


"""config=tf.ConfigProto(log_device_placement=True)"""
with tf.compat.v1.Session() as sess:

    UNET = Model(sess, SEED)

    UNET.compile()

    # print('Training...')
    # UNET.train(X_train, Y_train[:,:,:,1:3], X_val, Y_val[:,:,:,1:3])

    # Loading model.
    print('Loading model...')
    load_path = 'checkpoints/2021-05-17_11_22_53/'
    UNET.load(load_path)

    # print('Predicting training set...')
    X_train = X_train[0:20,:,:,:]
    pred = UNET.sample(X_train)
    pred = np.concatenate([X_train,pred], axis=3)
    save_lab_images(pred, filename="image/train_{}/after.png")

    print('Predicting validation set...')
    X_val = X_val[0:20,:,:,:]
    pred = UNET.sample(X_val)
    pred = np.concatenate([X_val,pred], axis=3)
    save_lab_images(pred, filename="image/val_{}/after.png")

    print('Predicting test set...')
    X_test = X_test[0:100,:,:,:]
    pred = UNET.sample(X_test)
    pred = np.concatenate([X_test,pred], axis=3)
    save_lab_images(pred, filename="images/test/Unet_{}.png")




