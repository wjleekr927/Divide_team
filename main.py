import random
import numpy as np

from collections import defaultdict
from options import args_parser_main

if __name__ == '__main__':
    # Parse args (from options.py)
    args = args_parser_main()

    member_list = []

    f = open("./member_list.txt", 'r', encoding='UTF8')
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        member_list.append(line)
    f.close

    # 총 멤버 수
    total_num = len(member_list)

    # 조 구성 (조합) 받기
    total_sum = 0
    config_team = defaultdict(list)
    print("총 {} 명\n".format(total_num))

    while total_sum != total_num:
        per_team = int(input("한 조에 몇 명? "))
        total_team = int(input("총 몇 조? "))
        config_team[per_team].append(total_team)
        total_sum += total_team * per_team
        if total_sum == total_num:
            print(">> 현재 인원: {} 명 \n".format(total_sum))
            matrix_config = []
            # 같은 key로 중복되면 합쳐서 하나로 받도록.
            for key, value in config_team.items():
                matrix_config.append([key,sum(value)])
            
            print(">> 조 인원 구성: ")
            for comb in matrix_config:
                print("{} 명 씩 {} 조".format(comb[0],comb[1]))

            print("\n======== 조원 구성 조합 완료 ========\n")
            break
        elif total_sum > total_num:
            print(">> 현재 인원: {} 명 \n".format(total_sum))
            print(">> 총원: {} 명 \n".format(total_num))
            raise Exception("총원 수를 초과하였습니다.")
        print(">> 현재 인원: {} 명 \n".format(total_sum))

    member_list = np.array(member_list)
    idx_list = np.zeros(total_num )
    idx_list[:args.special_num] = 1
    member_dict = dict(zip(member_list, idx_list))
    
    print("분류된 명단(선 배정): ")
    for key, value in member_dict.items():
        if value == 1:
            print(key)

    # 인원 구성 조합에 따른 matrix 생성
    max_num_per_team , total_team = 0, 0

    for item in matrix_config:
        if max_num_per_team < item[0]:
            max_num_per_team = item[0]
        total_team += item[1]

    matrix_entry = np.full((total_team,max_num_per_team),'',dtype='<U3')
    
    special_group = member_list[:args.special_num]
    normal_group = member_list[args.special_num:]

    # 행렬의 행 보다 special_group에 속한 인원 수가 더 많다면,
    if len(special_group) > matrix_entry.shape[0]:
        random.shuffle(special_group)
        special_select = special_group[:matrix_entry.shape[0]]
        normal_group = np.append(normal_group,special_group[matrix_entry.shape[0]:])
    else:
        special_select = special_group

    # 마지막 열에 random 하게 선 배정
    special_idx = np.random.choice(matrix_entry.shape[0], len(special_select), replace=False)
    for idx in range(len(special_idx)):
        matrix_entry[:,-1][special_idx[idx]] = special_select[idx]
    random.shuffle(normal_group)

    # 나머지 팀원 배정
    total_team_idx = 0
    for config_list in matrix_config:
        for team_idx in range(config_list[1]):
            until_idx = config_list[0]
            # 마지막 열에 '' 이 아닌 성분이 있다면,
            if matrix_entry[total_team_idx, -1] != '':
                until_idx -= 1
            matrix_entry[total_team_idx,:until_idx] = normal_group[:until_idx]
            normal_group = np.delete(normal_group,range(until_idx))
            total_team_idx += 1
    
    final_entry = matrix_entry.tolist()

    for team_number in range(total_team):
        while '' in final_entry[team_number]:
            final_entry[team_number].remove('')
        print("\n{}조: {}".format(team_number + 1, final_entry[team_number]))