import Algorithmia


def publish_algo(mgmt_api_key, api_address, algo_schema, algo_name, algo_hash):
    client = Algorithmia.client(api_key=mgmt_api_key, api_address=api_address)

    algo = client.algo("{}/{}".format(algo_name, algo_hash))
    results = algo.versions(1, published=True).results
    if len(results) > 0:
        cur_version = results[0]['version_info']
        print("--- last release version : {} ---".format(cur_version))
    else:
        print("--- working with fresh project (no previous release found)")

    if algo_schema not in ["major", "minor", "revision"]:
        raise Exception("{} is not considered a valid algorithm version schema".format(algo_schema))
    print("--- releasing new {}".format(algo_schema))
    algo.publish(version_info={"version_type": algo_schema, "release_notes": "automatically deployed by CI"}, settings={"royalty_microcredits": 0}, details={"label": "CICD"})
    latest_version = algo.versions(1, published=True).results[0]['version_info']
    print("--- new version {} successfully published".format(latest_version))
