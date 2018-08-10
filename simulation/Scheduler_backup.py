STATION_TABLE = []
from itertools import combinations
import numpy as np


class Scheduler:
    def __init__(self, total, n, p, alpha, beta):
        # self.opt = opt
        self.station_num = n
        self.time = p
        self.total = total
        self.station_table = init_table(n, p)
        self.alpha = alpha
        self.beta = beta
        self.last_assignment = np.array([0] * n)
        self.virtual_model = init_table(n, p)
        self.last_q = 0
        self.w1 = 1.0

    def naive_scheduler(self, sample_matrix, usage_vector):
        # not related to sample_matrix
        assignment = [int(x / sum(usage_vector) * self.total) for x in usage_vector]
        assignment[-1] = self.total - sum(assignment[:-1])
        self.last_assignment = assignment
        return assignment

    def greedy_scheduler(self, true_model_sample, usage_vector):
        self.virtual_model = np.ceil(self.alpha * self.virtual_model + (1-self.alpha) *true_model_sample)
        # print(self.virtual_model)
        # extract feature from virtual model.
        # print(true_model_sample.size)
        # print(usage_vector.size)
        if sum(self.last_assignment) == 0:
            temp_ass = np.ones((1, self.station_num)) * int(self.total / self.station_num)
            self.last_assignment = temp_ass[0]
            return self.last_assignment
        else:
            f, Q_val = Q(self.virtual_model, self.last_assignment, self.w1)
            # print("compute %d", Q_val)

            true_rewards = sum(usage_vector)
            diff = true_rewards - Q_val
            self.w1 = self.w1 + self.beta*diff*f[0]
            # self.w1 = 1
            # find action(generating)
            # print(self.w1)
            action_candidate = [self.last_assignment / sum(self.last_assignment)]
            for _ in range(34):
                # print(self.last_assignment.shape)
                random_vct = np.abs(np.random.randn(self.last_assignment.shape[0]))
                # print(random_vct.shape)
                action_candidate.append(random_vct / sum(random_vct))
            for iter in range(6):
                # print("iter")
                action_candidate = generation(action_candidate, self.virtual_model, self.total, self.w1)
                # print(action_candidate)
                action_candidate = ooxx(action_candidate)
                # print(action_candidate)

        # print(1, )
        # print("after generation")
        assignment = action_candidate[0]
        self.last_assignment = assignment
        # print(assignment)
        return assignment


def generation(cdd, vm, total, w):
    action = []
    qvals = np.array([0] * 20).astype(float)
    for i in range(20):
        action_now = normalize_with_weight(cdd[i], total)
        f, Qval = Q(vm, action_now, w)
        qvals[i] = Qval
        action.append(action_now)

    index = (np.argsort(qvals))

    action_ooxx = []
    for i in range(5):
        action_ooxx.append(action[index[19 - i]])
    # print(max(qvals), end='->')
    return action_ooxx


def random_seq(a, b, n):
    s = []
    while(len(s) < n):
        x = np.random.randint(a, b)
        if x not in s:
            s.append(x)
    return s


def ooxx(tobe_ooxx):
    change_number = 5
    new_candidate = []
    for cdd in tobe_ooxx:
        new_candidate.append(cdd.copy())

    for comb in combinations(tobe_ooxx, 2):
        rand_seq = random_seq(0, comb[0].shape[0], change_number)
        for j in rand_seq:
            temp = comb[0][j]
            comb[0][j] = comb[1][j]
            comb[1][j] = temp
        new_candidate.append(comb[0].copy())
        new_candidate.append(comb[1].copy())
    return new_candidate




def Q(vm, a, w):
    f1 = sum(simulate(vm, a))
    return [f1], w*f1


def normalize_with_weight(vet, total):
    temp = np.floor(vet / sum(vet) * total)
    temp[-1] = total - sum(temp[:-1])
    return temp


def simulate(model, assignment):
    usage = np.zeros(assignment.shape)
    left = assignment.astype('float64')
    for t in range(model.shape[0]):
        trans_matrix = model[t]
        # print(trans_matrix)
        buffer = np.zeros(assignment.shape)
        for i in range(model.shape[1]):
            # maybe leave
            total_leave = min(left[i], sum(trans_matrix[i]))
            # print(total_leave)
            if (sum(trans_matrix[i]) == 0):
                continue
            temp_trans = np.floor(trans_matrix[i] / sum(trans_matrix[i]) * total_leave)
            temp_trans[-1] = (total_leave - sum(temp_trans[:-1]))
            # print(sum(temp_trans) == total_leave)
            left[i] -= total_leave
            for j in range(model.shape[1]):
                # print(buffer, temp_trans[i])
                buffer[j] += temp_trans[j]
        usage += buffer
        # print(sum(buffer))
        left += buffer
        # print(sum(left), sum(buffer))
    return usage


def init_table(n, p):
    return np.ones((p, n, n)) * 100

def main():
    alpha = 0.9
    sche = Scheduler(10000, 10, 72, alpha)
    sample_matrix = init_table(10, 72)
    usage_vector = np.array([100] * 10)
    usage_vector[0] = 0
    print(usage_vector)
    sample_matrix[:, 0, :] = 0

    # print(sample_matrix[0])
    # print(simulate(sample_matrix, usage_vector))

    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)
    sche.greedy_scheduler(sample_matrix, usage_vector)

    
if __name__ == '__main__':
    main()
    # a = np.array([1, 2, 3, 4, 5, 3, 4, 5, 6, 7, 7, 8, 9])
    # b = np.array([2, 3, 4, 5, 6, 7, 7, 8, 9, 9, 0, 0, 1])
    # c = np.array([0, 7, 2, 5, 6, 7, 7, 5, 6, 7, 7, 8, 9])
    # for i in (ooxx([a, b, c])):
    #     print(i)

