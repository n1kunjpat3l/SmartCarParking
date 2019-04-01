""" Image classification with Inception. """
# Classify image and decrement the parking spot if a vehicle is detected in the image

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import re
import numpy as np
import tensorflow as tf
import sys
import time

print ("   Processing Image...")
vehicleStatus = sys.argv[1]
IMAGENET_FOLDER='/home/pi/carparking/imagenet'
carData=[]
predict=[]
maxLimit=50
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
FLAGS = tf.app.flags.FLAGS
tf.logging.set_verbosity(tf.logging.ERROR)
tf.app.flags.DEFINE_string(
    'model_dir',IMAGENET_FOLDER,
    """Path to classify_image_graph_def.pb, """
    """imagenet_synset_to_human_label_map.txt, and """
    """imagenet_2012_challenge_label_map_proto.pbtxt.""")
tf.app.flags.DEFINE_string('image_file', '/home/pi/carparking/images/image.jpg',
                           """Absolute path to image file.""")
tf.app.flags.DEFINE_integer('num_top_predictions', 5,
                            """Display this many predictions.""")


class NodeLookup(object):
    """Converts integer node ID's to human readable labels."""

    def __init__(self,
                 label_lookup_path=None,
                 uid_lookup_path=None):
        if not label_lookup_path:
            label_lookup_path = os.path.join(
                FLAGS.model_dir,
                'imagenet_2012_challenge_label_map_proto.pbtxt')
        if not uid_lookup_path:
            uid_lookup_path = os.path.join(
                FLAGS.model_dir, 'imagenet_synset_to_human_label_map.txt')
        self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

    def load(self, label_lookup_path, uid_lookup_path):
        if not tf.gfile.Exists(uid_lookup_path):
            tf.logging.fatal('File does not exist %s', uid_lookup_path)
        if not tf.gfile.Exists(label_lookup_path):
            tf.logging.fatal('File does not exist %s', label_lookup_path)

        # Loads mapping from string UID to human-readable string
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        p = re.compile(r'[n\d]*[ \S,]*')
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            uid = parsed_items[0]
            human_string = parsed_items[2]
            uid_to_human[uid] = human_string

        # Loads mapping from string UID to integer node ID.
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal('Failed to locate: %s', val)
            name = uid_to_human[val]
            node_id_to_name[key] = name

        return node_id_to_name

    def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]


def create_graph():
    with tf.gfile.FastGFile(os.path.join(
            FLAGS.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')  # noqa


def run_inference_on_image(image, external_run=False):
    if not tf.gfile.Exists(image):
        tf.logging.fatal('File does not exist %s', image)
    image_data = tf.gfile.FastGFile(image, 'rb').read()
    create_graph()

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)
        node_lookup = NodeLookup()
        top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
        for node_id in top_k:
            human_string = node_lookup.id_to_string(node_id)
            score = predictions[node_id]
            if external_run:
                return str(human_string).split(',')[0]
                
            else:
                #print('%s (score = %.5f)' % (human_string, score))
                #print(human_string);
                #print(human_string)
                predict.extend(x.strip() for x in (human_string).split(','))
        
        #store classification data in database
        #print(str(predict))
        from saveClassification import save
        save(str(predict))
        
        #if car is detected then decrement the car parking spot
        checkPredictions()
          
         
def checkPredictions():
    x=list(set(carData).intersection(predict))
    if len(x) > 0:
        print("   Vehicle Detected !! Updating Parking Spot")
        if vehicleStatus == 'in':
            os.system("python Decrement.py")
        elif vehicleStatus == 'out':
            os.system("python Increment.py")
        else:
            Print("check Input !!")
    else:
        print("   No Vehicle Detected!!")
        

def main(_):
    predict = []
    maxLimit=50
    getTextFile() #get text file data
    #for x in carData:
    #    print(x)
    start = time.clock()
    if FLAGS.image_file:
        image = FLAGS.image_file
        #print(run_inference_on_image(image))
        run_inference_on_image(image)        
    else:
        print("No image file specified! (Usage: --image_file=IMAGE_FILE.jpg)")
    end = time.clock()
    taken=end-start
    print ("time taken to process image:"+str(taken))
        

def getTextFile():
    f = open ("cars.txt","r")
    for line in f:
        carData.append(line.strip())


def external_run(image):
    best_guess = run_inference_on_image(image, external_run=True)
    return best_guess


if __name__ == '__main__':
    tf.app.run()