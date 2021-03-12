#!/usr/bin/env python3

"""
Implementation of the MANEPI algorithm as described in: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5694110
Author: Nerius Ilmonas
Date: 09/03/2021
"""

# Import all required data structures
import random
from structures import Event, FrequentEpisodePrefixTree, FrequentEpisodePrefixTreeNode


def manepi(event_sequence, min_sup, event_types):
    """
    Performs the MANEPI+ algorithm on a given
    event sequence with a defined support
    threshold and returns the results
    frequent episode prefix tree.

    args:
        event_sequence: The event sequence to perform the algorithm on.
        min_sup: The minimum support threshold.
    """

    # Create an empty FETP
    fept = FrequentEpisodePrefixTree()

    # Find all 1-episodes
    frequent_one_episodes = find_frequent_one_episodes(
        event_sequence, event_types, min_sup)

    for event_type, occurrences in frequent_one_episodes.items():
        # For simple 1-episodes, the support value is always just going to be the
        # length of the set of their occurrences
        node = fept.insert(event_type, occurrences, len(occurrences))

        grow(fept, node, frequent_one_episodes, min_sup)

    fept.output_to_file()
    return


def find_frequent_one_episodes(event_sequence, event_types, min_sup):
    """
    Finds all the frequent 1-episodes in the event sequence.
    """

    # Create a dictionary of event_types mapped to occurrences
    frequent_one_episodes = {event_type: [] for event_type in event_types}

    # Fill occurrence array
    for event in event_sequence:
        frequent_one_episodes[event.type].append([event.time] * 2)

    # Filter out all the episodes that don't have support >= min_sup
    return dict(filter(lambda episode: len(episode[1]) >= min_sup, frequent_one_episodes.items()))


def grow(fept, prefix_node, frequent_one_episodes, min_sup):
    """
    Expands a given node, adding onto the tree
    all the frequent episodes with the given
    node as a prefix.
    """
    for event_type, occurrences in frequent_one_episodes.items():

        # Concatenate the two episodes
        label = prefix_node.label + event_type

        # Grow our pattern and get the minimal occurrences of the new pattern
        minimal_occurrences = concat_minimal_occurrences(
            prefix_node, event_type, occurrences)

        # If the pattern has no minimal occurrences, don't try to grow it
        if not minimal_occurrences:
            continue

        # Check if the pattern is considered frequent (support >= min_sup)
        support = calculate_support(minimal_occurrences)
        if support >= min_sup:

            # If it is, create a new FEPT node and add it as a child of the current node
            node = fept.insert(label, minimal_occurrences, support)

            #MANEPI+ Optimisations
            # continue_growth = True
            # for i in range(1, len(label)):
            #     suffix = fept.get(label[i:])

            #     if not suffix:
            #         break

            #     # Case 1
            #     if suffix.support > prefix_node.support:
            #         break
            #     elif suffix.support <= prefix_node.support and not fept.exists(suffix.label):
            #         continue_growth = False
            #         break
            #     else:
            #         continue_growth = False
            #         break

            # if not continue_growth:
            #     continue

            # Grow the new pattern further
            grow(fept, node, frequent_one_episodes, min_sup)

    # All frequent patterns have now been found
    return


def concat_minimal_occurrences(episode_a, label, occurrences):
    """
    Computes the minimal occurences for a concatenation of episodes
    """

    # Initialise required variables
    b_minimal_occurrences = []
    a_minimal_occurrences = episode_a.minimal_occurrences
    a_minimal_occurrences_length = len(a_minimal_occurrences)
    i = 0

    for occurrence in occurrences:
        for j in range(i, a_minimal_occurrences_length):
            if a_minimal_occurrences[j][-1] < occurrence[0] and ((j < a_minimal_occurrences_length - 1 and a_minimal_occurrences[j + 1][-1] >= occurrence[0]) or j >= a_minimal_occurrences_length - 1):
                b_minimal_occurrences.append(
                    [a_minimal_occurrences[j][0], occurrence[0]])
                i = j
                break

    return b_minimal_occurrences


def calculate_support(occurrences):
    """
    Computes the cardinality of the largets
    set of minimal and non-overlapping
    occurrences.
    """

    i = 0
    j = 1
    support = 1
    length = len(occurrences)
    while j < length - 1:
        for k in range(j, length):
            if occurrences[i][-1] < occurrences[k][0]:
                support += 1
                i = k
                j = i + 1

            j += 1

    return support


event_types = ["A", "B", "C", "D", "E"]
# event_sequence = [Event("D", 0), Event("C", 1), Event("A", 2), Event("A", 3), Event("D", 4), Event("A", 5), Event("E", 6), Event("E", 7), Event("A", 8), Event("B", 9), Event("D", 10), Event("E", 11), Event("D", 12), Event("B", 13), Event("C", 14), Event("A", 15), Event("D", 16), Event("A", 17), Event("C", 18), Event("B", 19), Event("E", 20), Event("C", 21), Event("E", 22), Event("A", 23), Event("D", 24), Event("A", 25), Event("A", 26), Event("C", 27), Event("A", 28), Event("B", 29), Event("A", 30), Event("E", 31), Event("E", 32), Event("E", 33), Event("B", 34), Event("A", 35), Event("B", 36), Event("A", 37), Event("C", 38), Event("C", 39), Event("E", 40), Event("E", 41), Event("C", 42), Event("B", 43), Event("A", 44), Event("D", 45), Event("D", 46), Event("D", 47), Event("C", 48), Event("A", 49), Event("A", 50), Event("D", 51), Event("D", 52), Event("C", 53), Event("E", 54), Event("C", 55), Event("D", 56), Event("A", 57), Event("A", 58), Event("B", 59), Event("A", 60), Event("C", 61), Event("D", 62), Event("C", 63), Event("E", 64), Event("C", 65), Event("B", 66), Event("E", 67), Event("B", 68), Event("E", 69), Event("C", 70), Event("E", 71), Event("A", 72), Event("D", 73), Event("D", 74), Event("E", 75), Event("D", 76), Event("D", 77), Event("D", 78), Event("E", 79), Event("B", 80), Event("E", 81), Event("D", 82), Event("E", 83), Event("D", 84), Event("E", 85), Event("B", 86), Event("A", 87), Event("E", 88), Event("D", 89), Event("D", 90), Event("A", 91), Event("B", 92), Event("B", 93), Event("A", 94), Event("A", 95), Event("E", 96), Event("B", 97), Event("D", 98), Event("B", 99), Event("A", 100), Event("D", 101), Event("B", 102), Event("B", 103), Event("A", 104), Event("A", 105), Event("D", 106), Event("E", 107), Event("E", 108), Event("C", 109), Event("C", 110), Event("D", 111), Event("B", 112), Event("A", 113), Event("B", 114), Event("B", 115), Event("A", 116), Event("B", 117), Event("D", 118), Event("E", 119), Event("D", 120), Event("C", 121), Event("A", 122), Event("E", 123), Event("A", 124), Event("A", 125), Event("D", 126), Event("D", 127), Event("A", 128), Event("C", 129), Event("D", 130), Event("A", 131), Event("E", 132), Event("C", 133), Event("D", 134), Event("D", 135), Event("C", 136), Event("A", 137), Event("B", 138), Event("C", 139), Event("E", 140), Event("C", 141), Event("A", 142), Event("D", 143), Event("D", 144), Event("C", 145), Event("D", 146), Event("E", 147), Event("B", 148), Event("A", 149), Event("D", 150), Event("A", 151), Event("E", 152), Event("B", 153), Event("E", 154), Event("B", 155), Event("B", 156), Event("C", 157), Event("D", 158), Event("B", 159), Event("D", 160), Event("B", 161), Event("A", 162), Event("E", 163), Event("A", 164), Event("C", 165), Event("E", 166), Event("A", 167), Event("D", 168), Event("A", 169), Event("B", 170), Event("B", 171), Event("A", 172), Event("E", 173), Event("A", 174), Event("C", 175), Event("B", 176), Event("E", 177), Event("A", 178), Event("B", 179), Event("A", 180), Event("E", 181), Event("E", 182), Event("D", 183), Event("A", 184), Event("A", 185), Event("E", 186), Event("A", 187), Event("B", 188), Event("B", 189), Event("C", 190), Event("C", 191), Event("B", 192), Event("D", 193), Event("C", 194), Event("A", 195), Event("A", 196), Event("E", 197), Event("B", 198), Event("E", 199), Event("C", 200), Event("D", 201), Event("A", 202), Event("C", 203), Event("C", 204), Event("B", 205), Event("B", 206), Event("A", 207), Event("D", 208), Event("A", 209), Event("B", 210), Event("B", 211), Event("C", 212), Event("B", 213), Event("D", 214), Event("B", 215), Event("A", 216), Event("C", 217), Event("D", 218), Event("A", 219), Event("E", 220), Event("C", 221), Event("C", 222), Event("C", 223), Event("E", 224), Event("C", 225), Event("B", 226), Event("C", 227), Event("B", 228), Event("C", 229), Event("A", 230), Event("B", 231), Event("E", 232), Event("A", 233), Event("C", 234), Event("D", 235), Event("E", 236), Event("E", 237), Event("A", 238), Event("A", 239), Event("C", 240), Event("B", 241), Event("C", 242), Event("E", 243), Event("C", 244), Event("C", 245), Event("C", 246), Event("D", 247), Event("D", 248), Event("C", 249), Event("B", 250), Event("A", 251), Event("E", 252), Event("A", 253), Event("A", 254), Event("E", 255), Event("A", 256), Event("A", 257), Event("A", 258), Event("C", 259), Event("A", 260), Event("A", 261), Event("D", 262), Event("B", 263), Event("A", 264), Event("D", 265), Event("E", 266), Event("E", 267), Event("B", 268), Event("E", 269), Event("B", 270), Event("A", 271), Event("E", 272), Event("C", 273), Event("E", 274), Event("E", 275), Event("C", 276), Event("A", 277), Event("C", 278), Event("C", 279), Event("E", 280), Event("D", 281), Event("C", 282), Event("B", 283), Event("E", 284), Event("B", 285), Event("E", 286), Event("D", 287), Event("D", 288), Event("D", 289), Event("B", 290), Event("A", 291), Event("E", 292), Event("D", 293), Event("D", 294), Event("D", 295), Event("E", 296), Event("C", 297), Event("A", 298), Event("A", 299), Event("B", 300), Event("D", 301), Event("D", 302), Event("C", 303), Event("B", 304), Event("A", 305), Event("A", 306), Event("A", 307), Event("D", 308), Event("A", 309), Event("C", 310), Event("D", 311), Event("B", 312), Event("D", 313), Event("D", 314), Event("D", 315), Event("A", 316), Event("E", 317), Event("B", 318), Event("D", 319), Event("C", 320), Event("E", 321), Event("B", 322), Event("A", 323), Event("D", 324), Event("C", 325), Event("E", 326), Event("C", 327), Event("C", 328), Event("D", 329), Event("B", 330), Event("C", 331), Event("C", 332), Event("B", 333), Event("D", 334), Event("B", 335), Event("D", 336), Event("E", 337), Event("D", 338), Event("E", 339), Event("E", 340), Event("A", 341), Event("E", 342), Event("A", 343), Event("E", 344), Event("C", 345), Event("A", 346), Event("A", 347), Event("A", 348), Event("A", 349), Event("B", 350), Event("E", 351), Event("A", 352), Event("C", 353), Event("B", 354), Event("D", 355), Event("D", 356), Event("C", 357), Event("E", 358), Event("D", 359), Event("B", 360), Event("A", 361), Event("D", 362), Event("A", 363), Event("C", 364), Event("B", 365), Event("C", 366), Event("D", 367), Event("B", 368), Event("E", 369), Event("B", 370), Event("C", 371), Event("C", 372), Event("D", 373), Event("B", 374), Event("C", 375), Event("E", 376), Event("A", 377), Event("E", 378), Event("B", 379), Event("D", 380), Event("C", 381), Event("A", 382), Event("B", 383), Event("E", 384), Event("A", 385), Event("B", 386), Event("B", 387), Event("A", 388), Event("A", 389), Event("B", 390), Event("E", 391), Event("E", 392), Event("B", 393), Event("D", 394), Event("D", 395), Event("A", 396), Event("D", 397), Event("E", 398), Event("B", 399), Event("E", 400), Event("C", 401), Event("D", 402), Event("E", 403), Event("C", 404), Event("B", 405), Event("C", 406), Event("A", 407), Event("A", 408), Event("A", 409), Event("D", 410), Event("C", 411), Event("C", 412), Event("B", 413), Event("B", 414), Event("A", 415), Event("D", 416), Event("A", 417), Event("D", 418), Event("E", 419), Event("E", 420), Event("E", 421), Event("B", 422), Event("C", 423), Event("C", 424), Event("D", 425), Event("E", 426), Event("E", 427), Event("B", 428), Event("D", 429), Event("E", 430), Event("E", 431), Event("B", 432), Event("B", 433), Event("B", 434), Event("B", 435), Event("B", 436), Event("B", 437), Event("A", 438), Event("A", 439), Event("A", 440), Event("D", 441), Event("A", 442), Event("D", 443), Event("D", 444), Event("D", 445), Event("B", 446), Event("B", 447), Event("A", 448), Event("B", 449), Event("D", 450), Event("D", 451), Event("E", 452), Event("A", 453), Event("B", 454), Event("B", 455), Event("C", 456), Event("C", 457), Event("E", 458), Event("B", 459), Event("A", 460), Event("B", 461), Event("B", 462), Event("A", 463), Event("E", 464), Event("C", 465), Event("D", 466), Event("D", 467), Event("A", 468), Event("E", 469), Event("E", 470), Event("E", 471), Event("D", 472), Event("D", 473), Event("B", 474), Event("E", 475), Event("E", 476), Event("C", 477), Event("B", 478), Event("B", 479), Event("E", 480), Event("E", 481), Event("C", 482), Event("A", 483), Event("B", 484), Event("A", 485), Event("C", 486), Event("E", 487), Event("B", 488), Event("D", 489), Event("D", 490), Event("C", 491), Event("B", 492), Event("E", 493), Event("A", 494), Event("D", 495), Event("E", 496), Event("D", 497), Event("B", 498), Event("B", 499), Event("A", 500), Event("C", 501), Event(
#     "D", 502), Event("B", 503), Event("C", 504), Event("D", 505), Event("B", 506), Event("E", 507), Event("D", 508), Event("D", 509), Event("E", 510), Event("B", 511), Event("B", 512), Event("D", 513), Event("A", 514), Event("A", 515), Event("C", 516), Event("A", 517), Event("C", 518), Event("E", 519), Event("C", 520), Event("D", 521), Event("E", 522), Event("D", 523), Event("E", 524), Event("B", 525), Event("C", 526), Event("A", 527), Event("D", 528), Event("C", 529), Event("E", 530), Event("A", 531), Event("D", 532), Event("C", 533), Event("C", 534), Event("E", 535), Event("E", 536), Event("E", 537), Event("A", 538), Event("B", 539), Event("C", 540), Event("C", 541), Event("D", 542), Event("B", 543), Event("B", 544), Event("C", 545), Event("A", 546), Event("B", 547), Event("B", 548), Event("A", 549), Event("B", 550), Event("B", 551), Event("E", 552), Event("A", 553), Event("D", 554), Event("B", 555), Event("B", 556), Event("C", 557), Event("D", 558), Event("D", 559), Event("A", 560), Event("A", 561), Event("A", 562), Event("A", 563), Event("E", 564), Event("D", 565), Event("C", 566), Event("E", 567), Event("B", 568), Event("D", 569), Event("E", 570), Event("D", 571), Event("D", 572), Event("E", 573), Event("C", 574), Event("D", 575), Event("C", 576), Event("D", 577), Event("A", 578), Event("E", 579), Event("B", 580), Event("C", 581), Event("D", 582), Event("E", 583), Event("C", 584), Event("D", 585), Event("E", 586), Event("C", 587), Event("E", 588), Event("D", 589), Event("E", 590), Event("D", 591), Event("A", 592), Event("A", 593), Event("D", 594), Event("B", 595), Event("A", 596), Event("D", 597), Event("E", 598), Event("B", 599), Event("A", 600), Event("C", 601), Event("A", 602), Event("B", 603), Event("C", 604), Event("D", 605), Event("B", 606), Event("B", 607), Event("E", 608), Event("A", 609), Event("D", 610), Event("A", 611), Event("D", 612), Event("E", 613), Event("E", 614), Event("D", 615), Event("D", 616), Event("C", 617), Event("B", 618), Event("C", 619), Event("C", 620), Event("A", 621), Event("B", 622), Event("B", 623), Event("E", 624), Event("C", 625), Event("C", 626), Event("D", 627), Event("D", 628), Event("E", 629), Event("A", 630), Event("B", 631), Event("D", 632), Event("E", 633), Event("D", 634), Event("B", 635), Event("B", 636), Event("D", 637), Event("C", 638), Event("D", 639), Event("D", 640), Event("A", 641), Event("B", 642), Event("A", 643), Event("B", 644), Event("C", 645), Event("E", 646), Event("B", 647), Event("A", 648), Event("A", 649), Event("C", 650), Event("A", 651), Event("A", 652), Event("B", 653), Event("A", 654), Event("B", 655), Event("D", 656), Event("C", 657), Event("E", 658), Event("D", 659), Event("A", 660), Event("B", 661), Event("B", 662), Event("E", 663), Event("C", 664), Event("C", 665), Event("B", 666), Event("D", 667), Event("A", 668), Event("E", 669), Event("E", 670), Event("E", 671), Event("E", 672), Event("C", 673), Event("B", 674), Event("B", 675), Event("E", 676), Event("E", 677), Event("D", 678), Event("B", 679), Event("B", 680), Event("C", 681), Event("E", 682), Event("D", 683), Event("C", 684), Event("B", 685), Event("C", 686), Event("C", 687), Event("C", 688), Event("C", 689), Event("A", 690), Event("A", 691), Event("B", 692), Event("C", 693), Event("B", 694), Event("A", 695), Event("B", 696), Event("D", 697), Event("B", 698), Event("D", 699), Event("B", 700), Event("B", 701), Event("A", 702), Event("B", 703), Event("C", 704), Event("C", 705), Event("E", 706), Event("A", 707), Event("B", 708), Event("D", 709), Event("B", 710), Event("C", 711), Event("A", 712), Event("B", 713), Event("C", 714), Event("B", 715), Event("E", 716), Event("E", 717), Event("D", 718), Event("B", 719), Event("D", 720), Event("B", 721), Event("B", 722), Event("D", 723), Event("D", 724), Event("E", 725), Event("E", 726), Event("E", 727), Event("E", 728), Event("E", 729), Event("A", 730), Event("D", 731), Event("B", 732), Event("E", 733), Event("D", 734), Event("A", 735), Event("A", 736), Event("E", 737), Event("C", 738), Event("E", 739), Event("A", 740), Event("D", 741), Event("A", 742), Event("D", 743), Event("B", 744), Event("B", 745), Event("E", 746), Event("C", 747), Event("A", 748), Event("B", 749), Event("B", 750), Event("C", 751), Event("C", 752), Event("E", 753), Event("C", 754), Event("B", 755), Event("A", 756), Event("C", 757), Event("B", 758), Event("E", 759), Event("E", 760), Event("C", 761), Event("D", 762), Event("A", 763), Event("A", 764), Event("B", 765), Event("B", 766), Event("E", 767), Event("D", 768), Event("E", 769), Event("E", 770), Event("E", 771), Event("A", 772), Event("A", 773), Event("A", 774), Event("B", 775), Event("A", 776), Event("A", 777), Event("C", 778), Event("C", 779), Event("C", 780), Event("A", 781), Event("A", 782), Event("C", 783), Event("E", 784), Event("C", 785), Event("A", 786), Event("E", 787), Event("D", 788), Event("D", 789), Event("D", 790), Event("A", 791), Event("B", 792), Event("C", 793), Event("C", 794), Event("E", 795), Event("C", 796), Event("C", 797), Event("E", 798), Event("E", 799), Event("D", 800), Event("A", 801), Event("B", 802), Event("C", 803), Event("E", 804), Event("D", 805), Event("B", 806), Event("B", 807), Event("E", 808), Event("A", 809), Event("B", 810), Event("B", 811), Event("A", 812), Event("C", 813), Event("C", 814), Event("E", 815), Event("A", 816), Event("E", 817), Event("A", 818), Event("E", 819), Event("D", 820), Event("A", 821), Event("C", 822), Event("B", 823), Event("B", 824), Event("C", 825), Event("E", 826), Event("E", 827), Event("B", 828), Event("C", 829), Event("B", 830), Event("D", 831), Event("E", 832), Event("A", 833), Event("B", 834), Event("E", 835), Event("A", 836), Event("D", 837), Event("B", 838), Event("D", 839), Event("A", 840), Event("B", 841), Event("C", 842), Event("A", 843), Event("C", 844), Event("B", 845), Event("D", 846), Event("A", 847), Event("E", 848), Event("E", 849), Event("A", 850), Event("E", 851), Event("C", 852), Event("D", 853), Event("D", 854), Event("A", 855), Event("B", 856), Event("A", 857), Event("B", 858), Event("E", 859), Event("D", 860), Event("B", 861), Event("E", 862), Event("B", 863), Event("D", 864), Event("B", 865), Event("A", 866), Event("D", 867), Event("A", 868), Event("E", 869), Event("B", 870), Event("E", 871), Event("E", 872), Event("E", 873), Event("E", 874), Event("B", 875), Event("A", 876), Event("E", 877), Event("A", 878), Event("A", 879), Event("E", 880), Event("D", 881), Event("D", 882), Event("A", 883), Event("B", 884), Event("D", 885), Event("E", 886), Event("A", 887), Event("B", 888), Event("A", 889), Event("C", 890), Event("C", 891), Event("A", 892), Event("E", 893), Event("E", 894), Event("D", 895), Event("B", 896), Event("E", 897), Event("C", 898), Event("A", 899), Event("A", 900), Event("A", 901), Event("D", 902), Event("E", 903), Event("E", 904), Event("B", 905), Event("D", 906), Event("C", 907), Event("B", 908), Event("B", 909), Event("C", 910), Event("E", 911), Event("B", 912), Event("A", 913), Event("A", 914), Event("B", 915), Event("C", 916), Event("D", 917), Event("E", 918), Event("A", 919), Event("A", 920), Event("D", 921), Event("D", 922), Event("B", 923), Event("E", 924), Event("A", 925), Event("B", 926), Event("D", 927), Event("D", 928), Event("B", 929), Event("D", 930), Event("B", 931), Event("B", 932), Event("A", 933), Event("A", 934), Event("D", 935), Event("B", 936), Event("D", 937), Event("B", 938), Event("D", 939), Event("D", 940), Event("D", 941), Event("B", 942), Event("D", 943), Event("E", 944), Event("D", 945), Event("C", 946), Event("C", 947), Event("D", 948), Event("C", 949), Event("B", 950), Event("B", 951), Event("A", 952), Event("A", 953), Event("D", 954), Event("E", 955), Event("A", 956), Event("D", 957), Event("E", 958), Event("C", 959), Event("B", 960), Event("C", 961), Event("D", 962), Event("E", 963), Event("B", 964), Event("D", 965), Event("B", 966), Event("C", 967), Event("A", 968), Event("D", 969), Event("C", 970), Event("E", 971), Event("A", 972), Event("B", 973), Event("B", 974), Event("B", 975), Event("C", 976), Event("B", 977), Event("C", 978), Event("E", 979), Event("D", 980), Event("B", 981), Event("A", 982), Event("D", 983), Event("A", 984), Event("B", 985), Event("A", 986), Event("E", 987), Event("E", 988), Event("A", 989), Event("C", 990), Event("A", 991), Event("C", 992), Event("C", 993), Event("A", 994), Event("C", 995), Event("D", 996), Event("B", 997), Event("B", 998), Event("A", 999)]
event_sequence = [Event("A", 1), Event("A", 2), Event("B", 3), Event(
    "D", 4), Event("A", 5), Event("C", 6), Event("B", 7), Event("E", 8), Event("A", 9), Event("C", 10), Event("B", 11), Event("A", 12), Event("C", 13)]
manepi(event_sequence, 2, event_types)
