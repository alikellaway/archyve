class LoadingBar:
    def __init__(self, total_steps, prefix='', suffix='', decimals=1, length=100, fill='█'):
        """
        Initialize the loading bar.
        :param total_steps: Total number of steps for the loading bar
        :param prefix: Prefix string for the loading bar (default: '')
        :param suffix: Suffix string for the loading bar (default: '')
        :param decimals: Number of decimal places to show in the percentage (default: 1)
        :param length: Length of the loading bar in characters (default: 100)
        :param fill: Character to use to fill the loading bar (default: '█')
        """
        self.total_steps = total_steps
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.current_step = 0

    def update(self, step):
        """
        Update the loading bar with the current step.
        :param step: Current step
        """
        self.current_step = step
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (step / float(self.total_steps)))
        filled_length = int(self.length * step // self.total_steps)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end='')
        if step == self.total_steps:
            print()q


# Example usage
if __name__ == '__main__':
    import time
    loading_bar = LoadingBar(10, prefix='Progress:', suffix='Complete', length=50)
    for i in range(11):
        loading_bar.update(i)
        time.sleep(0.1)
