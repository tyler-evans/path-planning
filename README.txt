------------------------------------------------------------------------------------------------------------------------

The results below are obtained by running an experiment which generates 10 different maps, which are then presented as
path finding problems to each of the solutions: QuadTree Decomposition + Rapidly Exploring Random Tree.

The two path Path Planning algorithms have parameters which can be tweaked which can alter the performance on the
respective problems.

=======================
QuadTree Decomposition:
=======================
Decomposition Resolution - Minimum subdivision size of a cell

Values: [1.0, 3.0, 5.0]

==============================
Rapidly Exploring Random Tree:
==============================
Step Size - The length of the step taken during each iteration of the path finding algorithm

Values: [1, 3, 5]

------------------------------------------------------------------------------------------------------------------------

The averages are taken over each algorithm's performance using the selected parameters on 10 Different Maps:

+---------------------------------------------------------------------------------------+
|         QUADTREE DECOMPOSITION | 10 Different Maps | Problem Size (100 x 100)         |
+-----------+--------------------------+----------------------+-------------------------+
| # Objects | Decomposition Resolution | Average Path Lengths | Average Times (Seconds) |
+-----------+--------------------------+----------------------+-------------------------+
|     10    |           1.0            |        49.168        |          1.316          |
|     10    |           3.0            |        49.298        |          0.353          |
|     10    |           5.0            |        48.791        |          0.097          |
|     20    |           1.0            |        62.189        |          2.891          |
|     20    |           3.0            |        61.435        |          0.701          |
|     20    |           5.0            |        59.904        |          0.163          |
|     40    |           1.0            |        45.106        |          5.954          |
|     40    |           3.0            |        43.813        |          1.432          |
|     40    |           5.0            |        43.163        |          0.318          |
|     60    |           1.0            |        58.236        |          9.491          |
|     60    |           3.0            |        56.929        |          2.370          |
|     60    |           5.0            |        55.904        |          0.436          |
+-----------+--------------------------+----------------------+-------------------------+

+-------------------------------------------------------------------------------+
|  RAPIDLY EXPLORING RANDOM TREE | 10 Different Maps | Problem Size (100 x 100) |
+---------------+---------------+------------------+----------------------------+
|   # Objects   |   Step Size   |   Path Length    |     Run-time (Seconds)     |
+---------------+---------------+------------------+----------------------------+
|       10      |       1       |      63.336      |           0.294            |
|       10      |       5       |      59.832      |           0.030            |
|       20      |       1       |      92.485      |           1.657            |
|       20      |       3       |      73.444      |           0.217            |
|       20      |       5       |      78.737      |           0.127            |
|       40      |       1       |      57.496      |           1.123            |
|       40      |       3       |      55.796      |           0.577            |
|       40      |       5       |      61.169      |           0.185            |
|       60      |       1       |      94.632      |           4.435            |
|       60      |       3       |      78.087      |           1.614            |
|       60      |       5       |      75.026      |           0.358            |
+---------------+---------------+------------------+----------------------------+