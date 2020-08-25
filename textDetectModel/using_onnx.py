import os
from net import Net
from torch.autograd import Variable
import torch.onnx
import torch
import torchvision

import onnx
import numpy as np
#import caffe2.python.onnx.backend as backend


path = os.path.dirname(os.path.realpath(__file__))
model_path = path+"/models/pictex_100.pt"
#model_path = path+"/models/pictexHELP_100.pt"
model = Net()
model.load_state_dict(torch.load(model_path))
model.cpu()
model.train(False)


dummy_input = Variable(torch.randn(1, 1, 32, 32))
output_torch = model(dummy_input)

torch.onnx.export(model,
                  dummy_input,
                  "testing3.onnx",
                  export_params=True,
                  verbose=True)

graph = onnx.load("testing3.onnx")
onnx.checker.check_model(graph)

"""
rep = backend.prepare(graph, device="CPU")
#output_onnx = rep.run(dummy_input.cpu().data.numpy().astype(np.float32))
output_onnx = rep.run(np.random.randn(1, 1, 32, 32).astype(np.float32))
print(
    np.argmax(output_onnx)
)
"""
import onnxruntime as nxrun
sess = nxrun.InferenceSession("testing3.onnx")

input_name = (sess.get_inputs()[0].name)
ximg = np.random.randn(1,1,32,32).astype(np.float32)
result = sess.run(None, {input_name: ximg})
print(np.argmax(result))