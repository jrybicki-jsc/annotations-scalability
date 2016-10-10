from functools import partial

from neo4j.v1 import GraphDatabase
import os


def clean_db(session):
    session.run(
        "MATCH (n) "
        "OPTIONAL MATCH (n)-[r]-() "
        "DELETE n,r;")


def create_constraints(session):
    session.run(
        "CREATE constraint on (target:Target) "
        "ASSERT target.jsonld_id is unique;")
    session.run(
        "CREATE constraint on (body:Body) "
        "ASSERT body.jsonld_id is unique;")


def connect():
    host = os.getenv("NEO_PORT_7687_TCP_ADDR", "localhost")
    port = os.getenv("NEO_PORT_7687_TCP_PORT", "7687")
    # docker run -d -p 7687:7687 -p 7474:7474 --env=NEO4J_AUTH=none neo4j
    driver = GraphDatabase.driver("bolt://%s:%s" % (host, port),
                                  auth=None,
                                  encrypted=False)
    session = driver.session()
    return session

class executor:
    def __enter__(self):
        self.graph = connect()
        create_constraints(self.graph)
        store_function = partial(store_annotation, graph=self.graph)
        retrieve_function_1 = partial(retrieve_annotation_by_target, graph=self.graph)
        retrieve_function_2 = partial(retrieve_annotation_by_body, graph=self.graph)
        return store_function, retrieve_function_1, retrieve_function_2

    def __exit__(self, exc_type, exc_val, exc_tb):
        disconnect(self.graph)



def disconnect(session):
    session.close()


def store_annotation(annotation, graph):
    result = graph.run(
        "MERGE (b:Body {jsonld_id: {body_id}}) "
        "MERGE (t:Target {jsonld_id: {target_id}}) "
        "CREATE UNIQUE (b)-[:ANNOTATES {created: {created}}]->(t);",
        {"body_id": annotation['body']['jsonld_id'],
         "target_id": annotation['target']['jsonld_id'],
         "created": annotation['created']
         }
    )
    return result


def retrieve_annotation_by_target(target_id, graph):
    result = graph.run(
        "MATCH (target:Target {jsonld_id: {id}})-[r]-(body:Body) "
        "RETURN target,r,body "
        "LIMIT 1",  # removed in the future
        {'id': target_id}
    )

    # return extract_annotation(result.single())
    return result


def retrieve_annotation_by_body(body_id, graph):
    result = graph.run(
        "MATCH (body:Body {jsonld_id: {id}})-[r]-(target:Target) "
        "RETURN body,r,target "
        "LIMIT 1",  # removed in the future
        {'id': body_id}
    )

    # return extract_annotation(result.single())
    return result


def extract_annotation(result):
    return dict(
        body={
            "jsonld_id": result['body']['jsonld_id']
        },
        target={
            "jsonld_id": result['target']['jsonld_id']
        },
        created=result['t']['created']
    )
