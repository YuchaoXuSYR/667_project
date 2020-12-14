
import numpy as np
import torch as tr
from torch.nn import Sequential, Conv2d, Linear, Flatten, LeakyReLU, Tanh,Dropout


def ChessNet(board_size):
    f = 3 * board_size * board_size
    m1=3 * board_size
    m2=board_size
    model = Sequential(
        Flatten(),
        Linear(f, f),
        LeakyReLU(),
        #Dropout(p=0.2),
        Linear(f, m1),
        LeakyReLU(),
        #Dropout(p=0.2),
        Linear(m1, m2),
        LeakyReLU(),
        #Dropout(p=0.2),
        Linear(m2, 1),
        #LeakyReLU(),
        #Dropout(p=0.2),
    )
    return model



def train_func(optimizer, net, x, y_targ):
    batch_size=800000
    size=len(x)//batch_size+1
    ylist=[]
    elist=[]
    for i in range(size):
        optimizer.zero_grad()
        input=x[batch_size*i:batch_size*i+batch_size]
        target = y_targ[batch_size * i:batch_size * i + batch_size]

        input = input.cuda()
        target = target.cuda()
        output = net(input)
        error= (output.float() - target.float()) ** 2
        error=error.sum()
        error.backward()
        optimizer.step()

        y = output.cpu()
        e=error.cpu()
        del output,error
        tr.cuda.empty_cache()


        ylist.append(y)
        elist.append(e)
    ylist=tr.cat(ylist)
    elist = tr.stack(elist)
    elist = elist.sum()
    return (ylist, elist)


def test_func( net, x, y_targ):
    batch_size=1000
    size=len(x)//batch_size+1
    ylist=[]
    elist=[]
    for i in range(size):
        input=x[batch_size*i:batch_size*i+batch_size]
        target = y_targ[batch_size * i:batch_size * i + batch_size]

        input = input.cuda()
        target = target.cuda()
        output = net(input)
        error= (output.float() - target.float()) ** 2
        error=error.sum()

        y = output.cpu()
        e=error.cpu()
        del output,error
        tr.cuda.empty_cache()


        ylist.append(y)
        elist.append(e)
    ylist=tr.cat(ylist)
    elist = tr.stack(elist)
    elist = elist.sum()
    return (ylist, elist)

if __name__ == "__main__":
    for board_size in range(8,13,1):
        net = ChessNet(board_size=board_size)

        import pickle as pk

        with open("data%d.pkl" % board_size, "rb") as f:
            (x, y_targ) = pk.load(f)

        # mean = tr.max(y_targ)
        # std = tr.std(y_targ)
        # y_targ = (y_targ - mean) / std

        min = tr.min(y_targ)
        max = tr.max(y_targ)

        y_targ = (y_targ - min) / (max - min)

        # Optimization loop
        # x=x.cuda()
        # y_targ=y_targ.cuda()
        net = net.cuda()
        optimizer = tr.optim.Adam(net.parameters())
        train_loss, test_loss = [], []
        shuffle = np.random.permutation(range(len(x)))
        split = 10
        train, test = shuffle[:-split], shuffle[-split:]
        for epoch in range(300):
            y_train, e_train = train_func(optimizer, net, x[train], y_targ[train])
            y_test, e_test = test_func(net, x[test], y_targ[test])
            if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
            train_loss.append(e_train.item() / (len(shuffle) - split))
            test_loss.append(e_test.item() / split)

        tr.save(net.state_dict(), "model%d.pth" % board_size)

        import matplotlib.pyplot as pt

        pt.clf()
        pt.plot(train_loss, 'b-')
        pt.plot(test_loss, 'r-')
        pt.legend(["Train", "Test"])
        pt.xlabel("Iteration")
        pt.ylabel("Average Loss")
        pt.savefig('loss%d.png'% board_size)

        # pt.show()
        pt.clf()
        pt.plot(y_train.cpu().detach().numpy(), y_targ[train].cpu().detach().numpy(), 'bo')
        pt.plot(y_test.cpu().detach().numpy(), y_targ[test].cpu().detach().numpy(), 'ro')
        pt.legend(["Train", "Test"])
        pt.xlabel("Actual output")
        pt.ylabel("Target output")
        pt.savefig('target%d.png'% board_size)
        # .show()




