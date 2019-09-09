# OpenNMT-py helper scripts

## eoat-corpusclean

For a given regex, removes lines in one file that match (defaults to [a-zA-Z] and then deletes the corresponding lines in the sister file.

## eoat-trains3.py

This runs a training session and copies data and model files out to s3 so that you can use spot instances for training and don't lose training data.

Before running, run `aws configure` to add your AWS credentials

Bucket names must be *globally* unique. Otherwise, you may see location constraint errors. Apparently, the reason you see location constraint errors and not collision errors is that the bucket you're colliding with is in another region.

Syncs changes to the S3 bucket you specified, if the bucket doesn't exist, it will create it: Note that this assumes you're using the current directory for model files unless you use --working_dir (or -w). Be aware that model and training files are quite large...

You're probably going to run this with nohup [command] & at the end so that it runs continuously, like:

nohup ~/epub-ocr-and-translate/onmt-helpers/eoat-trains3.py -e my-train.py-file-if-not-using-the-custom-AMI -i my-training-data-file -m my-model-prefix -t my-optional-saved-model-to-restart_step_90000.pt -c 1000 -s my-very-unique-s3-bucket &

run eoat-trains3.py --help for full list of options

I will probably update to support more training options in the future, this is just a first pass.

## eoat-getbuckets.py

Not sure why I'm even checking this in, but you can run this pretty quickly to list your current s3 buckets and verify your AWS environment before jumping into the eoat-trains3 nest

## eoat-onmtpost.py

This is a helper script to send and receive src and target data from the OpenNMT-py REST server described at http://forum.opennmt.net/t/simple-opennmt-py-rest-server/1392 and located in OpenNMT-py's parent directory (https://github.com/OpenNMT/OpenNMT-py/blob/master/server.py). Quick start:

```
pip install flask

mkdir OpenNMT-REST

cd OpenNMT-REST && mkdir available-models && cp [your_models.pt] available-models/

Create a conf.json file in available-models like:
{
    "models_root": "./available_models",
    "models": [
        {   
            "id": 100,
            "model": "lang1-lang2.pt",
            "timeout": 600,
	     "opt": {
                "batch_size": 1,
                "beam_size": 10
            }
	{
            "id": 101,
            "model": "lang2-lang1.pt",
            "timeout": 600,
             "opt": {
                "batch_size": 1,
                "beam_size": 10
            }

        }
    ]   
}
Note that there are GPU options and such you can add here, see the forum post for details. This is just for quick setup on a CPU-bound machine.

Export some variables (these are from the tutorial, you can change them if you like):
export HOST=127.0.0.1
export CONFIG="./available_models/conf.json" 
export URL_ROOT="/translator"
export PORT="5000"
export IP="0.0.0.0"

python server.py --ip $IP --port $PORT --url_root $URL_ROOT --config $CONFIG &

python eoat-onmtpost.py "I want to translate this string" [model number] 

(model number defaults to 100, only because that's what's in the example and what I cribbed; change to match whichever model id you used to label the model you want to use in conf.json)
