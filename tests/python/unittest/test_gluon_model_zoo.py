from __future__ import print_function
import mxnet as mx
from mxnet.gluon import nn
from mxnet.gluon.model_zoo.custom_layers import HybridConcurrent, Identity
from mxnet.gluon.model_zoo.vision import get_model


def test_concurrent():
    model = HybridConcurrent(concat_dim=1)
    model.add(nn.Dense(128, activation='tanh', in_units=10))
    model.add(nn.Dense(64, activation='tanh', in_units=10))
    model.add(nn.Dense(32, in_units=10))

    # symbol
    x = mx.sym.var('data')
    y = model(x)
    assert len(y.list_arguments()) == 7

    # ndarray
    model.collect_params().initialize(mx.init.Xavier(magnitude=2.24))
    x = model(mx.nd.zeros((32, 10)))
    assert x.shape == (32, 224)
    x.wait_to_read()


def test_identity():
    model = Identity()
    x = mx.nd.random_uniform(shape=(128, 33, 64))
    mx.test_utils.assert_almost_equal(model(x).asnumpy(),
                                      x.asnumpy())


def test_models():
    all_models = ['resnet18_v1', 'resnet34_v1', 'resnet50_v1', 'resnet101_v1', 'resnet152_v1',
                  'resnet18_v2', 'resnet34_v2', 'resnet50_v2', 'resnet101_v2', 'resnet152_v2',
                  'vgg11', 'vgg13', 'vgg16', 'vgg19',
                  'vgg11_bn', 'vgg13_bn', 'vgg16_bn', 'vgg19_bn',
                  'alexnet', 'inceptionv3',
                  'densenet121', 'densenet161', 'densenet169', 'densenet201',
                  'squeezenet1.0', 'squeezenet1.1']
    pretrained_to_test = set(['squeezenet1.1'])

    for model_name in all_models:
        test_pretrain = model_name in pretrained_to_test
        model = get_model(model_name, pretrained=test_pretrain)
        data_shape = (7, 3, 224, 224) if 'inception' not in model_name else (7, 3, 299, 299)
        print(model)
        if not test_pretrain:
            model.collect_params().initialize()
        model(mx.nd.random_uniform(shape=data_shape))


if __name__ == '__main__':
    import nose
    nose.runmodule()
