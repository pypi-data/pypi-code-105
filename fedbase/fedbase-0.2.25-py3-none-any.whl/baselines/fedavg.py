from fedbase.utils.data_loader import data_process, log
from fedbase.nodes.node import node
from fedbase.server.server import server_class
import torch
from torch.utils.data import DataLoader
import torch.optim as optim
import os


def run(dataset, batch_size, num_nodes, model, objective, optimizer, global_rounds, local_steps, device = torch.device('cuda' if torch.cuda.is_available() else 'cpu'), **split):
    dt = data_process(dataset)
    train_splited,test_splited = dt.split_dataset(num_nodes, split['split_para'], split['split_method'])

    server = server_class()
    server.assign_model(model(), device)

    nodes = [node(i) for i in range(num_nodes)]
    local_models = [model() for i in range(num_nodes)]
    local_loss = [objective() for i in range(num_nodes)]

    for i in range(num_nodes):
        # data
        # print(len(train_splited[i]), len(test_splited[i]))
        nodes[i].assign_train(DataLoader(train_splited[i], batch_size=batch_size, shuffle=True))
        nodes[i].assign_test(DataLoader(test_splited[i],batch_size=batch_size, shuffle=False))
        # model
        nodes[i].assign_model(local_models[i], device)
        # objective
        nodes[i].assign_objective(local_loss[i])
        # optim
        # nodes[i].assign_optim(optimizer(nodes[i].model.parameters()))
        nodes[i].assign_optim(optim.SGD(nodes[i].model.parameters(), lr=0.001, momentum=0.9))

    # initialize parameters to nodes
    server.distribute(nodes, list(range(num_nodes)))

    # train!
    for i in range(global_rounds):
        print('-------------------Global round %d start-------------------' % (i))
        # single-processing!
        for j in range(num_nodes):
            nodes[j].local_update_steps(local_steps, device)
        # server aggregation and distribution
        server.aggregate(nodes, list(range(num_nodes)), device)
        server.distribute(nodes, list(range(num_nodes)))
        # test accuracy
        for j in range(num_nodes):
            nodes[j].local_test(device)
        server.acc(nodes, list(range(num_nodes)))

    # log
    log(os.path.basename(__file__)[:-3] + '_' + str(dataset) +'_' + split['split_method'] +'_' + str(split['split_para']) , nodes, server)