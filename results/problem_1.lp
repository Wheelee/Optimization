\ Model fuel_replenishment_problem_1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  10 x[0,1,1,1,1] + 10 x[0,1,1,1,2] + 10 x[0,1,1,2,1] + 10 x[0,1,1,2,2]
   + 12 x[0,2,1,1,1] + 12 x[0,2,1,1,2] + 12 x[0,2,1,2,1] + 12 x[0,2,1,2,2]
   + 10 x[1,0,1,1,1] + 10 x[1,0,1,1,2] + 10 x[1,0,1,2,1] + 10 x[1,0,1,2,2]
   + 8 x[1,2,1,1,1] + 8 x[1,2,1,1,2] + 8 x[1,2,1,2,1] + 8 x[1,2,1,2,2]
   + 12 x[2,0,1,1,1] + 12 x[2,0,1,1,2] + 12 x[2,0,1,2,1] + 12 x[2,0,1,2,2]
   + 8 x[2,1,1,1,1] + 8 x[2,1,1,1,2] + 8 x[2,1,1,2,1] + 8 x[2,1,1,2,2]
Subject To
 stock_balance[1,gazole,1]: I[1,gazole,1] - q[1,gazole,1,1,1,1]
   - q[1,gazole,1,2,1,1] - q[1,gazole,1,1,2,1] - q[1,gazole,1,2,2,1]
   = -2500
 safety_stock[1,gazole,1]: I[1,gazole,1] >= 500
 tank_capacity[1,gazole,1]: I[1,gazole,1] <= 12000
 capacity_before_consumption[1,gazole,1]: q[1,gazole,1,1,1,1]
   + q[1,gazole,1,2,1,1] + q[1,gazole,1,1,2,1] + q[1,gazole,1,2,2,1]
   <= 11000
 stock_balance[1,gazole,2]: - I[1,gazole,1] + I[1,gazole,2]
   - q[1,gazole,1,1,1,2] - q[1,gazole,1,2,1,2] - q[1,gazole,1,1,2,2]
   - q[1,gazole,1,2,2,2] = -3500
 safety_stock[1,gazole,2]: I[1,gazole,2] >= 500
 tank_capacity[1,gazole,2]: I[1,gazole,2] <= 12000
 capacity_before_consumption[1,gazole,2]: I[1,gazole,1]
   + q[1,gazole,1,1,1,2] + q[1,gazole,1,2,1,2] + q[1,gazole,1,1,2,2]
   + q[1,gazole,1,2,2,2] <= 12000
 stock_balance[1,sp95,1]: I[1,sp95,1] - q[1,sp95,1,1,1,1]
   - q[1,sp95,1,2,1,1] - q[1,sp95,1,1,2,1] - q[1,sp95,1,2,2,1] = -1500
 safety_stock[1,sp95,1]: I[1,sp95,1] >= 250
 tank_capacity[1,sp95,1]: I[1,sp95,1] <= 8000
 capacity_before_consumption[1,sp95,1]: q[1,sp95,1,1,1,1]
   + q[1,sp95,1,2,1,1] + q[1,sp95,1,1,2,1] + q[1,sp95,1,2,2,1] <= 7500
 stock_balance[1,sp95,2]: - I[1,sp95,1] + I[1,sp95,2] - q[1,sp95,1,1,1,2]
   - q[1,sp95,1,2,1,2] - q[1,sp95,1,1,2,2] - q[1,sp95,1,2,2,2] = -2000
 safety_stock[1,sp95,2]: I[1,sp95,2] >= 250
 tank_capacity[1,sp95,2]: I[1,sp95,2] <= 8000
 capacity_before_consumption[1,sp95,2]: I[1,sp95,1] + q[1,sp95,1,1,1,2]
   + q[1,sp95,1,2,1,2] + q[1,sp95,1,1,2,2] + q[1,sp95,1,2,2,2] <= 8000
 stock_balance[2,gazole,1]: I[2,gazole,1] - q[2,gazole,1,1,1,1]
   - q[2,gazole,1,2,1,1] - q[2,gazole,1,1,2,1] - q[2,gazole,1,2,2,1]
   = -2500
 safety_stock[2,gazole,1]: I[2,gazole,1] >= 500
 tank_capacity[2,gazole,1]: I[2,gazole,1] <= 12000
 capacity_before_consumption[2,gazole,1]: q[2,gazole,1,1,1,1]
   + q[2,gazole,1,2,1,1] + q[2,gazole,1,1,2,1] + q[2,gazole,1,2,2,1]
   <= 11000
 stock_balance[2,gazole,2]: - I[2,gazole,1] + I[2,gazole,2]
   - q[2,gazole,1,1,1,2] - q[2,gazole,1,2,1,2] - q[2,gazole,1,1,2,2]
   - q[2,gazole,1,2,2,2] = -3500
 safety_stock[2,gazole,2]: I[2,gazole,2] >= 500
 tank_capacity[2,gazole,2]: I[2,gazole,2] <= 12000
 capacity_before_consumption[2,gazole,2]: I[2,gazole,1]
   + q[2,gazole,1,1,1,2] + q[2,gazole,1,2,1,2] + q[2,gazole,1,1,2,2]
   + q[2,gazole,1,2,2,2] <= 12000
 stock_balance[2,sp95,1]: I[2,sp95,1] - q[2,sp95,1,1,1,1]
   - q[2,sp95,1,2,1,1] - q[2,sp95,1,1,2,1] - q[2,sp95,1,2,2,1] = -1500
 safety_stock[2,sp95,1]: I[2,sp95,1] >= 250
 tank_capacity[2,sp95,1]: I[2,sp95,1] <= 8000
 capacity_before_consumption[2,sp95,1]: q[2,sp95,1,1,1,1]
   + q[2,sp95,1,2,1,1] + q[2,sp95,1,1,2,1] + q[2,sp95,1,2,2,1] <= 7500
 stock_balance[2,sp95,2]: - I[2,sp95,1] + I[2,sp95,2] - q[2,sp95,1,1,1,2]
   - q[2,sp95,1,2,1,2] - q[2,sp95,1,1,2,2] - q[2,sp95,1,2,2,2] = -2000
 safety_stock[2,sp95,2]: I[2,sp95,2] >= 250
 tank_capacity[2,sp95,2]: I[2,sp95,2] <= 8000
 capacity_before_consumption[2,sp95,2]: I[2,sp95,1] + q[2,sp95,1,1,1,2]
   + q[2,sp95,1,2,1,2] + q[2,sp95,1,1,2,2] + q[2,sp95,1,2,2,2] <= 8000
 compartment_assignment[1,1,1,1]: - a[1,1,1] + z[1,gazole,1,1,1,1]
   + z[1,sp95,1,1,1,1] + z[2,gazole,1,1,1,1] + z[2,sp95,1,1,1,1] <= 0
 compartment_assignment[1,2,1,1]: - a[1,1,1] + z[1,gazole,1,2,1,1]
   + z[1,sp95,1,2,1,1] + z[2,gazole,1,2,1,1] + z[2,sp95,1,2,1,1] <= 0
 compartment_assignment[1,1,1,2]: - a[1,1,2] + z[1,gazole,1,1,1,2]
   + z[1,sp95,1,1,1,2] + z[2,gazole,1,1,1,2] + z[2,sp95,1,1,1,2] <= 0
 compartment_assignment[1,2,1,2]: - a[1,1,2] + z[1,gazole,1,2,1,2]
   + z[1,sp95,1,2,1,2] + z[2,gazole,1,2,1,2] + z[2,sp95,1,2,1,2] <= 0
 compartment_assignment[1,1,2,1]: - a[1,2,1] + z[1,gazole,1,1,2,1]
   + z[1,sp95,1,1,2,1] + z[2,gazole,1,1,2,1] + z[2,sp95,1,1,2,1] <= 0
 compartment_assignment[1,2,2,1]: - a[1,2,1] + z[1,gazole,1,2,2,1]
   + z[1,sp95,1,2,2,1] + z[2,gazole,1,2,2,1] + z[2,sp95,1,2,2,1] <= 0
 compartment_assignment[1,1,2,2]: - a[1,2,2] + z[1,gazole,1,1,2,2]
   + z[1,sp95,1,1,2,2] + z[2,gazole,1,1,2,2] + z[2,sp95,1,1,2,2] <= 0
 compartment_assignment[1,2,2,2]: - a[1,2,2] + z[1,gazole,1,2,2,2]
   + z[1,sp95,1,2,2,2] + z[2,gazole,1,2,2,2] + z[2,sp95,1,2,2,2] <= 0
 compartment_capacity[1,gazole,1,1,1,1]: - 4000 z[1,gazole,1,1,1,1]
   + q[1,gazole,1,1,1,1] <= 0
 assignment_visit[1,gazole,1,1,1,1]: - y[1,1,1,1] + z[1,gazole,1,1,1,1]
   <= 0
 compartment_capacity[1,gazole,1,2,1,1]: - 3000 z[1,gazole,1,2,1,1]
   + q[1,gazole,1,2,1,1] <= 0
 assignment_visit[1,gazole,1,2,1,1]: - y[1,1,1,1] + z[1,gazole,1,2,1,1]
   <= 0
 compartment_capacity[1,gazole,1,1,1,2]: - 4000 z[1,gazole,1,1,1,2]
   + q[1,gazole,1,1,1,2] <= 0
 assignment_visit[1,gazole,1,1,1,2]: - y[1,1,1,2] + z[1,gazole,1,1,1,2]
   <= 0
 compartment_capacity[1,gazole,1,2,1,2]: - 3000 z[1,gazole,1,2,1,2]
   + q[1,gazole,1,2,1,2] <= 0
 assignment_visit[1,gazole,1,2,1,2]: - y[1,1,1,2] + z[1,gazole,1,2,1,2]
   <= 0
 compartment_capacity[1,gazole,1,1,2,1]: - 4000 z[1,gazole,1,1,2,1]
   + q[1,gazole,1,1,2,1] <= 0
 assignment_visit[1,gazole,1,1,2,1]: - y[1,1,2,1] + z[1,gazole,1,1,2,1]
   <= 0
 compartment_capacity[1,gazole,1,2,2,1]: - 3000 z[1,gazole,1,2,2,1]
   + q[1,gazole,1,2,2,1] <= 0
 assignment_visit[1,gazole,1,2,2,1]: - y[1,1,2,1] + z[1,gazole,1,2,2,1]
   <= 0
 compartment_capacity[1,gazole,1,1,2,2]: - 4000 z[1,gazole,1,1,2,2]
   + q[1,gazole,1,1,2,2] <= 0
 assignment_visit[1,gazole,1,1,2,2]: - y[1,1,2,2] + z[1,gazole,1,1,2,2]
   <= 0
 compartment_capacity[1,gazole,1,2,2,2]: - 3000 z[1,gazole,1,2,2,2]
   + q[1,gazole,1,2,2,2] <= 0
 assignment_visit[1,gazole,1,2,2,2]: - y[1,1,2,2] + z[1,gazole,1,2,2,2]
   <= 0
 compartment_capacity[1,sp95,1,1,1,1]: - 4000 z[1,sp95,1,1,1,1]
   + q[1,sp95,1,1,1,1] <= 0
 assignment_visit[1,sp95,1,1,1,1]: - y[1,1,1,1] + z[1,sp95,1,1,1,1] <= 0
 compartment_capacity[1,sp95,1,2,1,1]: - 3000 z[1,sp95,1,2,1,1]
   + q[1,sp95,1,2,1,1] <= 0
 assignment_visit[1,sp95,1,2,1,1]: - y[1,1,1,1] + z[1,sp95,1,2,1,1] <= 0
 compartment_capacity[1,sp95,1,1,1,2]: - 4000 z[1,sp95,1,1,1,2]
   + q[1,sp95,1,1,1,2] <= 0
 assignment_visit[1,sp95,1,1,1,2]: - y[1,1,1,2] + z[1,sp95,1,1,1,2] <= 0
 compartment_capacity[1,sp95,1,2,1,2]: - 3000 z[1,sp95,1,2,1,2]
   + q[1,sp95,1,2,1,2] <= 0
 assignment_visit[1,sp95,1,2,1,2]: - y[1,1,1,2] + z[1,sp95,1,2,1,2] <= 0
 compartment_capacity[1,sp95,1,1,2,1]: - 4000 z[1,sp95,1,1,2,1]
   + q[1,sp95,1,1,2,1] <= 0
 assignment_visit[1,sp95,1,1,2,1]: - y[1,1,2,1] + z[1,sp95,1,1,2,1] <= 0
 compartment_capacity[1,sp95,1,2,2,1]: - 3000 z[1,sp95,1,2,2,1]
   + q[1,sp95,1,2,2,1] <= 0
 assignment_visit[1,sp95,1,2,2,1]: - y[1,1,2,1] + z[1,sp95,1,2,2,1] <= 0
 compartment_capacity[1,sp95,1,1,2,2]: - 4000 z[1,sp95,1,1,2,2]
   + q[1,sp95,1,1,2,2] <= 0
 assignment_visit[1,sp95,1,1,2,2]: - y[1,1,2,2] + z[1,sp95,1,1,2,2] <= 0
 compartment_capacity[1,sp95,1,2,2,2]: - 3000 z[1,sp95,1,2,2,2]
   + q[1,sp95,1,2,2,2] <= 0
 assignment_visit[1,sp95,1,2,2,2]: - y[1,1,2,2] + z[1,sp95,1,2,2,2] <= 0
 compartment_capacity[2,gazole,1,1,1,1]: - 4000 z[2,gazole,1,1,1,1]
   + q[2,gazole,1,1,1,1] <= 0
 assignment_visit[2,gazole,1,1,1,1]: - y[2,1,1,1] + z[2,gazole,1,1,1,1]
   <= 0
 compartment_capacity[2,gazole,1,2,1,1]: - 3000 z[2,gazole,1,2,1,1]
   + q[2,gazole,1,2,1,1] <= 0
 assignment_visit[2,gazole,1,2,1,1]: - y[2,1,1,1] + z[2,gazole,1,2,1,1]
   <= 0
 compartment_capacity[2,gazole,1,1,1,2]: - 4000 z[2,gazole,1,1,1,2]
   + q[2,gazole,1,1,1,2] <= 0
 assignment_visit[2,gazole,1,1,1,2]: - y[2,1,1,2] + z[2,gazole,1,1,1,2]
   <= 0
 compartment_capacity[2,gazole,1,2,1,2]: - 3000 z[2,gazole,1,2,1,2]
   + q[2,gazole,1,2,1,2] <= 0
 assignment_visit[2,gazole,1,2,1,2]: - y[2,1,1,2] + z[2,gazole,1,2,1,2]
   <= 0
 compartment_capacity[2,gazole,1,1,2,1]: - 4000 z[2,gazole,1,1,2,1]
   + q[2,gazole,1,1,2,1] <= 0
 assignment_visit[2,gazole,1,1,2,1]: - y[2,1,2,1] + z[2,gazole,1,1,2,1]
   <= 0
 compartment_capacity[2,gazole,1,2,2,1]: - 3000 z[2,gazole,1,2,2,1]
   + q[2,gazole,1,2,2,1] <= 0
 assignment_visit[2,gazole,1,2,2,1]: - y[2,1,2,1] + z[2,gazole,1,2,2,1]
   <= 0
 compartment_capacity[2,gazole,1,1,2,2]: - 4000 z[2,gazole,1,1,2,2]
   + q[2,gazole,1,1,2,2] <= 0
 assignment_visit[2,gazole,1,1,2,2]: - y[2,1,2,2] + z[2,gazole,1,1,2,2]
   <= 0
 compartment_capacity[2,gazole,1,2,2,2]: - 3000 z[2,gazole,1,2,2,2]
   + q[2,gazole,1,2,2,2] <= 0
 assignment_visit[2,gazole,1,2,2,2]: - y[2,1,2,2] + z[2,gazole,1,2,2,2]
   <= 0
 compartment_capacity[2,sp95,1,1,1,1]: - 4000 z[2,sp95,1,1,1,1]
   + q[2,sp95,1,1,1,1] <= 0
 assignment_visit[2,sp95,1,1,1,1]: - y[2,1,1,1] + z[2,sp95,1,1,1,1] <= 0
 compartment_capacity[2,sp95,1,2,1,1]: - 3000 z[2,sp95,1,2,1,1]
   + q[2,sp95,1,2,1,1] <= 0
 assignment_visit[2,sp95,1,2,1,1]: - y[2,1,1,1] + z[2,sp95,1,2,1,1] <= 0
 compartment_capacity[2,sp95,1,1,1,2]: - 4000 z[2,sp95,1,1,1,2]
   + q[2,sp95,1,1,1,2] <= 0
 assignment_visit[2,sp95,1,1,1,2]: - y[2,1,1,2] + z[2,sp95,1,1,1,2] <= 0
 compartment_capacity[2,sp95,1,2,1,2]: - 3000 z[2,sp95,1,2,1,2]
   + q[2,sp95,1,2,1,2] <= 0
 assignment_visit[2,sp95,1,2,1,2]: - y[2,1,1,2] + z[2,sp95,1,2,1,2] <= 0
 compartment_capacity[2,sp95,1,1,2,1]: - 4000 z[2,sp95,1,1,2,1]
   + q[2,sp95,1,1,2,1] <= 0
 assignment_visit[2,sp95,1,1,2,1]: - y[2,1,2,1] + z[2,sp95,1,1,2,1] <= 0
 compartment_capacity[2,sp95,1,2,2,1]: - 3000 z[2,sp95,1,2,2,1]
   + q[2,sp95,1,2,2,1] <= 0
 assignment_visit[2,sp95,1,2,2,1]: - y[2,1,2,1] + z[2,sp95,1,2,2,1] <= 0
 compartment_capacity[2,sp95,1,1,2,2]: - 4000 z[2,sp95,1,1,2,2]
   + q[2,sp95,1,1,2,2] <= 0
 assignment_visit[2,sp95,1,1,2,2]: - y[2,1,2,2] + z[2,sp95,1,1,2,2] <= 0
 compartment_capacity[2,sp95,1,2,2,2]: - 3000 z[2,sp95,1,2,2,2]
   + q[2,sp95,1,2,2,2] <= 0
 assignment_visit[2,sp95,1,2,2,2]: - y[2,1,2,2] + z[2,sp95,1,2,2,2] <= 0
 depot_departure[1,1,1]: - a[1,1,1] + x[0,1,1,1,1] + x[0,2,1,1,1] = 0
 depot_return[1,1,1]: - a[1,1,1] + x[1,0,1,1,1] + x[2,0,1,1,1] = 0
 depot_departure[1,1,2]: - a[1,1,2] + x[0,1,1,1,2] + x[0,2,1,1,2] = 0
 depot_return[1,1,2]: - a[1,1,2] + x[1,0,1,1,2] + x[2,0,1,1,2] = 0
 depot_departure[1,2,1]: - a[1,2,1] + x[0,1,1,2,1] + x[0,2,1,2,1] = 0
 depot_return[1,2,1]: - a[1,2,1] + x[1,0,1,2,1] + x[2,0,1,2,1] = 0
 depot_departure[1,2,2]: - a[1,2,2] + x[0,1,1,2,2] + x[0,2,1,2,2] = 0
 depot_return[1,2,2]: - a[1,2,2] + x[1,0,1,2,2] + x[2,0,1,2,2] = 0
 incoming_arc[1,1,1,1]: - y[1,1,1,1] + x[0,1,1,1,1] + x[2,1,1,1,1] = 0
 outgoing_arc[1,1,1,1]: - y[1,1,1,1] + x[1,0,1,1,1] + x[1,2,1,1,1] = 0
 active_visit[1,1,1,1]: - a[1,1,1] + y[1,1,1,1] <= 0
 incoming_arc[1,1,1,2]: - y[1,1,1,2] + x[0,1,1,1,2] + x[2,1,1,1,2] = 0
 outgoing_arc[1,1,1,2]: - y[1,1,1,2] + x[1,0,1,1,2] + x[1,2,1,1,2] = 0
 active_visit[1,1,1,2]: - a[1,1,2] + y[1,1,1,2] <= 0
 incoming_arc[1,1,2,1]: - y[1,1,2,1] + x[0,1,1,2,1] + x[2,1,1,2,1] = 0
 outgoing_arc[1,1,2,1]: - y[1,1,2,1] + x[1,0,1,2,1] + x[1,2,1,2,1] = 0
 active_visit[1,1,2,1]: - a[1,2,1] + y[1,1,2,1] <= 0
 incoming_arc[1,1,2,2]: - y[1,1,2,2] + x[0,1,1,2,2] + x[2,1,1,2,2] = 0
 outgoing_arc[1,1,2,2]: - y[1,1,2,2] + x[1,0,1,2,2] + x[1,2,1,2,2] = 0
 active_visit[1,1,2,2]: - a[1,2,2] + y[1,1,2,2] <= 0
 incoming_arc[2,1,1,1]: - y[2,1,1,1] + x[0,2,1,1,1] + x[1,2,1,1,1] = 0
 outgoing_arc[2,1,1,1]: - y[2,1,1,1] + x[2,0,1,1,1] + x[2,1,1,1,1] = 0
 active_visit[2,1,1,1]: - a[1,1,1] + y[2,1,1,1] <= 0
 incoming_arc[2,1,1,2]: - y[2,1,1,2] + x[0,2,1,1,2] + x[1,2,1,1,2] = 0
 outgoing_arc[2,1,1,2]: - y[2,1,1,2] + x[2,0,1,1,2] + x[2,1,1,1,2] = 0
 active_visit[2,1,1,2]: - a[1,1,2] + y[2,1,1,2] <= 0
 incoming_arc[2,1,2,1]: - y[2,1,2,1] + x[0,2,1,2,1] + x[1,2,1,2,1] = 0
 outgoing_arc[2,1,2,1]: - y[2,1,2,1] + x[2,0,1,2,1] + x[2,1,1,2,1] = 0
 active_visit[2,1,2,1]: - a[1,2,1] + y[2,1,2,1] <= 0
 incoming_arc[2,1,2,2]: - y[2,1,2,2] + x[0,2,1,2,2] + x[1,2,1,2,2] = 0
 outgoing_arc[2,1,2,2]: - y[2,1,2,2] + x[2,0,1,2,2] + x[2,1,1,2,2] = 0
 active_visit[2,1,2,2]: - a[1,2,2] + y[2,1,2,2] <= 0
 mtz_lower[1,1,1,1]: - y[1,1,1,1] + u[1,1,1,1] >= 0
 mtz_upper[1,1,1,1]: - 2 y[1,1,1,1] + u[1,1,1,1] <= 0
 mtz_lower[1,1,1,2]: - y[1,1,1,2] + u[1,1,1,2] >= 0
 mtz_upper[1,1,1,2]: - 2 y[1,1,1,2] + u[1,1,1,2] <= 0
 mtz_lower[1,1,2,1]: - y[1,1,2,1] + u[1,1,2,1] >= 0
 mtz_upper[1,1,2,1]: - 2 y[1,1,2,1] + u[1,1,2,1] <= 0
 mtz_lower[1,1,2,2]: - y[1,1,2,2] + u[1,1,2,2] >= 0
 mtz_upper[1,1,2,2]: - 2 y[1,1,2,2] + u[1,1,2,2] <= 0
 mtz_lower[2,1,1,1]: - y[2,1,1,1] + u[2,1,1,1] >= 0
 mtz_upper[2,1,1,1]: - 2 y[2,1,1,1] + u[2,1,1,1] <= 0
 mtz_lower[2,1,1,2]: - y[2,1,1,2] + u[2,1,1,2] >= 0
 mtz_upper[2,1,1,2]: - 2 y[2,1,1,2] + u[2,1,1,2] <= 0
 mtz_lower[2,1,2,1]: - y[2,1,2,1] + u[2,1,2,1] >= 0
 mtz_upper[2,1,2,1]: - 2 y[2,1,2,1] + u[2,1,2,1] <= 0
 mtz_lower[2,1,2,2]: - y[2,1,2,2] + u[2,1,2,2] >= 0
 mtz_upper[2,1,2,2]: - 2 y[2,1,2,2] + u[2,1,2,2] <= 0
 mtz_order[1,2,1,1,1]: y[2,1,1,1] + 2 x[1,2,1,1,1] + u[1,1,1,1]
   - u[2,1,1,1] <= 2
 mtz_order[2,1,1,1,1]: y[1,1,1,1] + 2 x[2,1,1,1,1] - u[1,1,1,1]
   + u[2,1,1,1] <= 2
 mtz_order[1,2,1,1,2]: y[2,1,1,2] + 2 x[1,2,1,1,2] + u[1,1,1,2]
   - u[2,1,1,2] <= 2
 mtz_order[2,1,1,1,2]: y[1,1,1,2] + 2 x[2,1,1,1,2] - u[1,1,1,2]
   + u[2,1,1,2] <= 2
 mtz_order[1,2,1,2,1]: y[2,1,2,1] + 2 x[1,2,1,2,1] + u[1,1,2,1]
   - u[2,1,2,1] <= 2
 mtz_order[2,1,1,2,1]: y[1,1,2,1] + 2 x[2,1,1,2,1] - u[1,1,2,1]
   + u[2,1,2,1] <= 2
 mtz_order[1,2,1,2,2]: y[2,1,2,2] + 2 x[1,2,1,2,2] + u[1,1,2,2]
   - u[2,1,2,2] <= 2
 mtz_order[2,1,1,2,2]: y[1,1,2,2] + 2 x[2,1,1,2,2] - u[1,1,2,2]
   + u[2,1,2,2] <= 2
Bounds
Binaries
 a[1,1,1] a[1,1,2] a[1,2,1] a[1,2,2] y[1,1,1,1] y[1,1,1,2] y[1,1,2,1]
 y[1,1,2,2] y[2,1,1,1] y[2,1,1,2] y[2,1,2,1] y[2,1,2,2] x[0,1,1,1,1]
 x[0,1,1,1,2] x[0,1,1,2,1] x[0,1,1,2,2] x[0,2,1,1,1] x[0,2,1,1,2]
 x[0,2,1,2,1] x[0,2,1,2,2] x[1,0,1,1,1] x[1,0,1,1,2] x[1,0,1,2,1]
 x[1,0,1,2,2] x[1,2,1,1,1] x[1,2,1,1,2] x[1,2,1,2,1] x[1,2,1,2,2]
 x[2,0,1,1,1] x[2,0,1,1,2] x[2,0,1,2,1] x[2,0,1,2,2] x[2,1,1,1,1]
 x[2,1,1,1,2] x[2,1,1,2,1] x[2,1,1,2,2] z[1,gazole,1,1,1,1]
 z[1,gazole,1,2,1,1] z[1,gazole,1,1,1,2] z[1,gazole,1,2,1,2]
 z[1,gazole,1,1,2,1] z[1,gazole,1,2,2,1] z[1,gazole,1,1,2,2]
 z[1,gazole,1,2,2,2] z[1,sp95,1,1,1,1] z[1,sp95,1,2,1,1] z[1,sp95,1,1,1,2]
 z[1,sp95,1,2,1,2] z[1,sp95,1,1,2,1] z[1,sp95,1,2,2,1] z[1,sp95,1,1,2,2]
 z[1,sp95,1,2,2,2] z[2,gazole,1,1,1,1] z[2,gazole,1,2,1,1]
 z[2,gazole,1,1,1,2] z[2,gazole,1,2,1,2] z[2,gazole,1,1,2,1]
 z[2,gazole,1,2,2,1] z[2,gazole,1,1,2,2] z[2,gazole,1,2,2,2]
 z[2,sp95,1,1,1,1] z[2,sp95,1,2,1,1] z[2,sp95,1,1,1,2] z[2,sp95,1,2,1,2]
 z[2,sp95,1,1,2,1] z[2,sp95,1,2,2,1] z[2,sp95,1,1,2,2] z[2,sp95,1,2,2,2]
End
