from producto import ollaGA


class functionsGA(ollaGA):
    def __init__(self):
        self.padres = []
        self.hijos = []

    def cruza(self, padre):
        self.padres.append(padre)
        
        if self.padres.__len__ == 2:
            self.hijos 
