from prettytable import PrettyTable


class DataTracker:

    def __init__(self, table_columns, results_data_frame, problem_size, display_plot_name):
        self.table = PrettyTable(table_columns)
        self.display_plot_name = display_plot_name
        self.title = "{} - Problem Size ({} x {})".format(display_plot_name, problem_size, problem_size)
        self.table.title = self.title
        self.results_data_frame = results_data_frame

    def __str__(self):
        for index, row in self.results_data_frame.iterrows():
            if self.display_plot_name == 'Quadtree Decomposition':
                self.table.add_row([int(row['map_id']), int(row['num_objects']), row['decomposition_size'], '%.3f' % row['path_length'], '%.3f' % row['time']])
            elif self.display_plot_name == 'Rapidly Exploring Random Tree':
                self.table.add_row([int(row['map_id']), int(row['num_objects']), int(row['step_size']), '%.3f' % row['path_length'], '%.3f' % row['time']])
        return str(self.table)
