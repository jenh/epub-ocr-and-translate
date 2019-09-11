# OpenNMT-py helper scripts

## eoat-corpusclean

For a given regex, removes lines in one file that match (defaults to [a-zA-Z] and then deletes the corresponding lines in the sister file. Use -r 'a-zA-Z' (where a-zA-Z is your regex) to remove lines that match. Use -k 'a-zA-Z' to keep lines that match.

## eoat-trains3.py

This runs a training session and copies data and model files out to s3 so that you can use spot instances for training and don't lose training data.

Before running, run `aws configure` to add your AWS credentials

Bucket names must be *globally* unique. Otherwise, you may see location constraint errors. Apparently, the reason you see location constraint errors and not collision errors is that the bucket you're colliding with is in another region.

Syncs changes to the S3 bucket you specified, if the bucket doesn't exist, it will create it: Note that this assumes you're using the current directory for model files unless you use --working_dir (or -w). Be aware that model and training files are quite large...

You're probably going to run this with nohup [command] & at the end so that it runs continuously, like:

nohup ~/epub-ocr-and-translate/onmt-helpers/eoat-trains3.py -e my-train.py-file-if-not-using-the-custom-AMI -i my-training-data-file -m my-model-prefix -t my-optional-saved-model-to-restart_step_90000.pt -c 1000 -s my-very-unique-s3-bucket &

run eoat-trains3.py --help for full list of options

I will probably update to support more training options in the future, this is just a first pass. OpenNMT recommends the following to replicate Google's result (but this script does not yet support them): 

python  train.py -data /tmp/de2/data -save_model /tmp/extra \
        -layers 6 -rnn_size 512 -word_vec_size 512 -transformer_ff 2048 -heads 8  \
        -encoder_type transformer -decoder_type transformer -position_encoding \
        -train_steps 200000  -max_generator_batches 2 -dropout 0.1 \
        -batch_size 4096 -batch_type tokens -normalization tokens  -accum_count 2 \
        -optim adam -adam_beta2 0.998 -decay_method noam -warmup_steps 8000 -learning_rate 2 \
        -max_grad_norm 0 -param_init 0  -param_init_glorot \
        -label_smoothing 0.1 -valid_steps 10000 -save_checkpoint_steps 10000 \
        -world_size 4 -gpu_ranks 0 1 2 3


## eoat-getbuckets.py

Not sure why I'm even checking this in, but you can run this pretty quickly to list your current s3 buckets and verify your AWS environment before jumping into the eoat-trains3 nest.

## eoat-onmtpost.py

This is a helper script to send and receive src and target data from the OpenNMT-py REST server described at http://forum.opennmt.net/t/simple-opennmt-py-rest-server/1392 and located in OpenNMT-py's parent directory (https://github.com/OpenNMT/OpenNMT-py/blob/master/server.py). Quick start:

```
pip install flask

mkdir OpenNMT-REST

cd OpenNMT-REST && mkdir available-models && cp [your_models.pt] available-models/

Create a conf.json file in available-models like:
{
    'models_root': './available_models',
    'models': [
        {   
            'id': 100,
            'model': 'lang1-lang2.pt',
            'timeout': 600,
	     'opt': {
                'batch_size': 1,
                'beam_size': 10
            }
	{
            'id': 101,
            'model': 'lang2-lang1.pt',
            'timeout': 600,
             'opt': {
                'batch_size': 1,
                'beam_size': 10
            }

        }
    ]   
}
```

Note that there are GPU options and such you can add here, see the forum post for details. This is just for quick setup on a CPU-bound machine (if you're moving machines a lot, can use an option of 'gpu': -1 for no GPU and set to 0,1 or whichever GPUs you're using when you're on a GPU-enabled system, but omitting the option seems to work, too).

Export some variables (these are from the tutorial, you can change them if you like):

```
export HOST=127.0.0.1
export CONFIG='./available_models/conf.json' 
export URL_ROOT='/translator'
export PORT='5000'
export IP='0.0.0.0'

python server.py --ip $IP --port $PORT --url_root $URL_ROOT --config $CONFIG &

python eoat-onmtpost.py 'I want to translate this string' [model number] 

```

(model number defaults to 100, only because that's what's in the example and what I cribbed; change to match whichever model id you used to label the model you want to use in conf.json)

## eoat-postprocess.py

This script will take a mixed sentence for input and translate untranslated pieces using a dictionary, returning the full sentence. Intended for use with eont-onmtpost.py: You send the untranslated sentence to onmt-post with replace_unk enabled in the server.py configuration. Take that output, and plug it into eoat-post-process.py, which will find the untranslated bits, search the sqlite3 database you specify for a match, then replace with the translation. You can run it with -u to show what it's translated literally.

### What you need to use it:

- Python 3 (tested with 3.6) with guess_language, guess_language_spirit, and pyenchant. PyEnchant is super important, guess_language doesn't guess <20 word sentences accurately without it.

- A sqlite3 dictionary file with a table that contains at least two columns, each column using the language code you're translating to/from. For example, if you were doing Spanish->English, you'd use 'es' as the column name for the Spanish word, and 'en' for its English translation.

- If you want to import your dictionary from a csv/tsv file with headers and don't want to create the schema from scratch (if you've just got two columns, no biggie...but if you're importing a file with multiple languages/tenses/etc, it's so much easier to just create the whole structure on import), a modern version of sqlite3 (the package on CentOS 7 is unfortunately very old, I had to rpm -ivh sqlite-3.8.11-1.fc21.x86_64.rpm  sqlite-devel-3.8.11-1.fc21.x86_64.rpm --force). I must reiterate that I do not recommend running *any* of my scripts on a machine you use for other things. Ephemeral EC2 instances and snapshots are your friends.

- Optionally, OpenNMT Simple REST Server with replace_unk enabled. This is the script's intended use, to take OpenNMT model-translated output and convert all of the untranslated bits literally. This will of course not be perfect, but...

### eoat-postprocess.py command line options:

  -h, --help            show this help message and exit
  -s SENTENCE, --sentence SENTENCE
                        Sentence to translate
  -l LANGUAGE, --language LANGUAGE
                        Source language (two-letter-code)
  -t TARGETLANGUAGE, --targetlanguage TARGETLANGUAGE
                        Target language, defaults to en
  -d DATABASE, --database DATABASE
                        SQLite3 dictionary database
  -T TABLE, --table TABLE
                        dictionary table name
  -u, --showunknowns    Surround post-processed words with brackets

