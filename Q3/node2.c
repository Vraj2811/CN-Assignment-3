#include <stdio.h>
#include <string.h>

extern struct rtpkt
{
    int sourceid;   /* id of sending router sending this pkt */
    int destid;     /* id of router to which pkt being sent
                       (must be an immediate neighbor) */
    int mincost[4]; /* min cost to node 0 ... 3 */
};

extern int TRACE;
extern int YES;
extern int NO;

struct distance_table
{
    int costs[4][4];
} dt2;

/* students to write the following two routines, and maybe some others */
#define INFINITY 999

extern float clocktime;

int connectcosts2[4] = {3, 1, 0, 2};
struct rtpkt pkt2[4];
int min_cost_2[4];

void calc_send_pkt2()
{
    int old_min_cost[4];
    memcpy(old_min_cost, min_cost_2, sizeof(min_cost_2));
    int change = 0;

    for (int i = 0; i < 4; i++)
    {
        min_cost_2[i] = dt2.costs[i][0];
        for (int j = 1; j < 4; j++)
        {
            min_cost_2[i] = min_cost_2[i] < dt2.costs[i][j] ? min_cost_2[i] : dt2.costs[i][j];
        }
    }

    for (int i = 0; i < 4; i++)
    {
        if (old_min_cost[i] != min_cost_2[i])
        {
            change = 1;
        }
    }
    if (change == 1)
    { // min cost changed, so send new packets
        // make the pkts
        for (int i = 0; i < 4; i++)
        {
            pkt2[i].sourceid = 2;
            pkt2[i].destid = i; // to all 4 coz all are connected
            memcpy(pkt2[i].mincost, min_cost_2, sizeof(min_cost_2));
        }
        // SEND PKTS TO ALL NEIGHBOURS
        for (int i = 0; i < 4; i++)
        {
            if (i != 2)
            {
                tolayer2(pkt2[i]);
                printf("At time t=%.3f, node %d sends packet to node %d with: (%d  %d  %d  %d)\n",
                       clocktime, pkt2[i].sourceid, pkt2[i].destid, pkt2[i].mincost[0], pkt2[i].mincost[1],
                       pkt2[i].mincost[2], pkt2[i].mincost[3]);
            }
        }
    }
    else
        printf("\nMinimum cost didn't change. No new packets are sent\n");
}

void rtinit2()
{
    printf("rtinit2() is called at time t=: %0.3f\n", clocktime);

    // Initialize the distance table with the direct costs
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            if (i == j)
                dt2.costs[i][j] = connectcosts2[i];
            else
                dt2.costs[i][j] = INFINITY;
        }
    }
    printdt2(&dt2);
    calc_send_pkt2();
}

void rtupdate2(rcvdpkt) struct rtpkt *rcvdpkt;

{
    int src = rcvdpkt->sourceid;
    int dest = rcvdpkt->destid;
    int mincost[4];
    for (int j = 0; j < 4; j++)
        mincost[j] = rcvdpkt->mincost[j];

    printf("rtupdate2() is called at time t=: %0.3f as node %d sent a pkt with (%d  %d  %d  %d)\n", clocktime, src,
           mincost[0], mincost[1], mincost[2], mincost[3]);

    int change;

    // update the distance table
    for (int i = 0; i < 4; i++)
    {
        int possibleValue = dt2.costs[src][src] + mincost[i]; // use the already calculated min_cost_0 path to all node
        // if(possibleValue < dt2.costs[i][src]){
        //     change = 1;
        if (possibleValue < INFINITY)
            dt2.costs[i][src] = possibleValue;
        else
            dt2.costs[i][src] = INFINITY;
        //}
    }

    // if(change == 1) {
    printdt2(&dt2);

    // Finally update the min_cost_2 path to all nodes
    calc_send_pkt2();
}

printdt2(dtptr) struct distance_table *dtptr;

{
    printf("                via     \n");
    printf("   D2 |    0     1    3 \n");
    printf("  ----|-----------------\n");
    printf("     0|  %3d   %3d   %3d\n", dtptr->costs[0][0],
           dtptr->costs[0][1], dtptr->costs[0][3]);
    printf("dest 1|  %3d   %3d   %3d\n", dtptr->costs[1][0],
           dtptr->costs[1][1], dtptr->costs[1][3]);
    printf("     3|  %3d   %3d   %3d\n", dtptr->costs[3][0],
           dtptr->costs[3][1], dtptr->costs[3][3]);
}

printmincost2()
{
    printf("Minimum cost from %d to other nodes are: %d %d %d %d\n", 2, min_cost_2[0], min_cost_2[1],
           min_cost_2[2], min_cost_2[3]);
}
