from collections import deque
from functools import lru_cache


class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map  # Mini mapa do jogo usado para navegação
       
        # Direções possíveis para o movimento (horizontal, vertical e diagonal)
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        
        # Grafo representando o mapa (será preenchido posteriormente)
        self.graph = {}
        self.get_graph()  # Inicializa o grafo com os caminhos disponíveis

    @lru_cache  # Otimiza a função armazenando os resultados de chamadas anteriores
    def get_path(self, start, goal):
        """
        Encontra o melhor caminho do ponto 'start' ao 'goal' usando BFS.
        Retorna o próximo passo na direção correta.
        """
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        # Remonta o caminho a partir do destino até a origem
        while step and step != start:
            path.append(step)
            step = self.visited[step]
        
        return path[-1]  # Retorna o próximo nó no caminho

    def bfs(self, start, goal, graph):
        """
        Algoritmo de busca em largura (BFS) para encontrar o caminho mais curto no grafo.
        Retorna um dicionário com os nós visitados e suas conexões.
        """
        queue = deque([start])  # Fila de nós a serem visitados
        visited = {start: None}  # Dicionário de nós visitados

        while queue:
            cur_node = queue.popleft()  # Remove o nó atual da fila
            if cur_node == goal:
                break  # Para a busca ao alcançar o objetivo

            # Obtém os nós vizinhos do nó atual
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                # Se o nó ainda não foi visitado e não está ocupado por um NPC, adiciona à fila
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = cur_node  # Registra de onde veio esse nó

        return visited  # Retorna os nós visitados e suas conexões

    def get_next_nodes(self, x, y):
        """
        Retorna uma lista de coordenadas válidas (não bloqueadas por paredes) ao redor de (x, y).
        """
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]

    def get_graph(self):
        """
        Cria o grafo do mapa do jogo, onde cada posição acessível é um nó conectado aos seus vizinhos.
        """
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:  # Se não for uma parede (célula vazia), adiciona ao grafo
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)
