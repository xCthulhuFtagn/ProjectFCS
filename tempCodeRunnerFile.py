deploy_analyzer = Process(name='Mempool analyzer',
                              target=analyze_trns,
                              args=(new_deploys_trns_queue, ),
                              daemon=True)