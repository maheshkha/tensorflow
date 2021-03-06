# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for TFGAN summaries."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from tensorflow.contrib.gan.python import namedtuples
from tensorflow.contrib.gan.python.eval.python import summaries_impl as summaries
from tensorflow.python.framework import ops
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import variable_scope
from tensorflow.python.ops import variables
from tensorflow.python.platform import test
from tensorflow.python.summary import summary


def generator_model(inputs):
  return variable_scope.get_variable('dummy_g', initializer=2.0) * inputs


def discriminator_model(inputs, _):
  return variable_scope.get_variable('dummy_d', initializer=2.0) * inputs


def get_gan_model():
  # TODO(joelshor): Find a better way of creating a variable scope.
  with variable_scope.variable_scope('generator') as gen_scope:
    pass
  with variable_scope.variable_scope('discriminator') as dis_scope:
    pass
  return namedtuples.GANModel(
      generator_inputs=array_ops.zeros([4, 32, 32, 3]),
      generated_data=array_ops.zeros([4, 32, 32, 3]),
      generator_variables=[variables.Variable(0), variables.Variable(1)],
      generator_scope=gen_scope,
      generator_fn=generator_model,
      real_data=array_ops.ones([4, 32, 32, 3]),
      discriminator_real_outputs=array_ops.ones([1, 2, 3]),
      discriminator_gen_outputs=array_ops.ones([1, 2, 3]),
      discriminator_variables=[variables.Variable(0)],
      discriminator_scope=dis_scope,
      discriminator_fn=discriminator_model)


class SummariesTest(test.TestCase):

  def testAddGanModelImageSummaries(self):
    summaries.add_gan_model_image_summaries(get_gan_model(), grid_size=2)

    self.assertEquals(5, len(ops.get_collection(ops.GraphKeys.SUMMARIES)))
    with self.test_session(use_gpu=True):
      variables.global_variables_initializer().run()
      summary.merge_all().eval()

  def testAddGanModelSummaries(self):
    summaries.add_gan_model_summaries(get_gan_model())

    self.assertEquals(3, len(ops.get_collection(ops.GraphKeys.SUMMARIES)))
    with self.test_session(use_gpu=True):
      variables.global_variables_initializer().run()
      summary.merge_all().eval()

  def testAddRegularizationLossSummaries(self):
    summaries.add_regularization_loss_summaries(get_gan_model())

    self.assertEquals(2, len(ops.get_collection(ops.GraphKeys.SUMMARIES)))
    with self.test_session(use_gpu=True):
      summary.merge_all().eval()

  # TODO(joelshor): Add correctness test.
  def testAddImageComparisonSummaries(self):
    summaries.add_image_comparison_summaries(
        get_gan_model(), display_diffs=True)

    self.assertEquals(1, len(ops.get_collection(ops.GraphKeys.SUMMARIES)))
    with self.test_session(use_gpu=True):
      summary.merge_all().eval()


if __name__ == '__main__':
  test.main()
