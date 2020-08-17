import csv
import datetime
from notion.client import NotionClient

def read_timetable(f):
    res = []
    reader = csv.DictReader(f)
    for row in reader: res.append(row)
    return res

def convert_property(name, value):
    if name == "date": return

def prepare_doc(row):
    doc = dict()
    doc["Name"] = row["name"]
    doc["Duration"] = int(row["duration"])
    d = "%s %s" % (row["date"], row["time"])
    doc["Finished at"] = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M")
    doc["Status"] = "Done"
    return doc

def publish_row(doc, collection):
    row = collection.add_row()
    row.icon = b'\xe2\x9c\x85'.decode("utf8")
    for k, v in doc.items():
        row.set_property(k, v)

def notion_connect(token):
    return NotionClient(token_v2=token)

def get_collection(client, collection_id):
    return client.get_collection(collection_id)

token = sys.argv[1]
collection_id = sys.argv[2]
fn = sys.argv[3]

timetable = read_timetable(open(fn))

collection = get_collection(notion_connect(token), collection_id)

doc = prepare_doc(timetable[0])
publish_row(doc, collection)
