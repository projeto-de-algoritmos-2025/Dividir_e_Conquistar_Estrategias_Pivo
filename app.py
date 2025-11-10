import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np
from pivot_strategy import PivotStrategy
from quick_select import quickselect
from quick_sort import quicksort


class QuickSelectVisualizer:
    def __init__(self, data, k, pivot_strategy_normal=None, pivot_name="Normal"):
        self.original_data = data.copy()
        self.data_normal = data.copy()
        self.data_median = data.copy()
        self.k = k
        self.pivot_strategy_normal = pivot_strategy_normal or PivotStrategy.last_element
        self.pivot_name = pivot_name
        self.steps_normal = []
        self.steps_median = []
        self.comparisons_normal = 0
        self.comparisons_median = 0
        self.partitions_normal = 0
        self.partitions_median = 0
        self.result_normal = None
        self.result_median = None
    
    def run_selects(self):
        stats_normal = {'comparisons': 0, 'partitions': 0}
        if len(self.data_normal) > 0:
            self.result_normal = quickselect(
                self.data_normal, 0, len(self.data_normal) - 1, self.k, 
                self.steps_normal, self.pivot_strategy_normal, stats_normal
            )
        self.comparisons_normal = stats_normal['comparisons']
        self.partitions_normal = stats_normal['partitions']
        
        stats_median = {'comparisons': 0, 'partitions': 0}
        if len(self.data_median) > 0:
            self.result_median = quickselect(
                self.data_median, 0, len(self.data_median) - 1, self.k, 
                self.steps_median, PivotStrategy.median_of_medians, stats_median
            )
        self.comparisons_median = stats_median['comparisons']
        self.partitions_median = stats_median['partitions']
    
    def animate(self, interval=200):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle(f'Comparação: QuickSelect ({self.pivot_name}) vs QuickSelect com Mediana das Medianas\nBuscando o {self.k+1}º menor elemento', 
                     fontsize=16, fontweight='bold')
        
        max_steps = max(len(self.steps_normal), len(self.steps_median))
        
        def update(frame):
            ax1.clear()
            ax2.clear()
            
            # QuickSelect Normal
            if frame < len(self.steps_normal):
                step = self.steps_normal[frame]
                arr = step['array']
                left = step['left']
                right = step['right']
                pivot_idx = step['pivot_idx']
                k = step['k']
                
                colors = ['lightgray'] * len(arr)
                for i in range(left, right + 1):
                    colors[i] = 'yellow'
                if pivot_idx < len(colors):
                    colors[pivot_idx] = 'red'
                if k < len(colors):
                    colors[k] = 'blue'
                
                if step['type'] == 'found':
                    colors[k] = 'green'
                
                bars1 = ax1.bar(range(len(arr)), arr, color=colors, edgecolor='black')
                title_suffix = ' - ENCONTRADO! ✓' if step['type'] == 'found' else ''
                ax1.set_title(f'QuickSelect ({self.pivot_name}){title_suffix}\nPasso {frame + 1}/{len(self.steps_normal)}', 
                             fontsize=14, fontweight='bold')
                ax1.set_ylabel('Valor', fontsize=12)
                ax1.set_xlabel(f'Comparações: {self.comparisons_normal} | Partições: {self.partitions_normal}', 
                              fontsize=11)
            else:
                arr = self.data_normal
                colors = ['lightgray'] * len(arr)
                colors[self.k] = 'green'
                bars1 = ax1.bar(range(len(arr)), arr, color=colors, edgecolor='black')
                ax1.set_title(f'QuickSelect ({self.pivot_name}) - COMPLETO ✓\nResultado: {self.result_normal}', 
                             fontsize=14, fontweight='bold', color='green')
                ax1.set_ylabel('Valor', fontsize=12)
                ax1.set_xlabel(f'Comparações: {self.comparisons_normal} | Partições: {self.partitions_normal}', 
                              fontsize=11)
            
            # QuickSelect com Mediana das Medianas
            if frame < len(self.steps_median):
                step = self.steps_median[frame]
                arr = step['array']
                left = step['left']
                right = step['right']
                pivot_idx = step['pivot_idx']
                k = step['k']
                
                colors = ['lightgray'] * len(arr)
                for i in range(left, right + 1):
                    colors[i] = 'lightyellow'
                if pivot_idx < len(colors):
                    colors[pivot_idx] = 'darkred'
                if k < len(colors):
                    colors[k] = 'blue'
                
                if step['type'] == 'found':
                    colors[k] = 'darkgreen'
                
                bars2 = ax2.bar(range(len(arr)), arr, color=colors, edgecolor='black')
                title_suffix = ' - ENCONTRADO! ✓' if step['type'] == 'found' else ''
                ax2.set_title(f'QuickSelect com Mediana das Medianas{title_suffix}\nPasso {frame + 1}/{len(self.steps_median)}', 
                             fontsize=14, fontweight='bold')
                ax2.set_ylabel('Valor', fontsize=12)
                ax2.set_xlabel(f'Comparações: {self.comparisons_median} | Partições: {self.partitions_median}', 
                              fontsize=11)
            else:
                arr = self.data_median
                colors = ['lightgray'] * len(arr)
                colors[self.k] = 'darkgreen'
                bars2 = ax2.bar(range(len(arr)), arr, color=colors, edgecolor='black')
                ax2.set_title(f'QuickSelect com Mediana das Medianas - COMPLETO ✓\nResultado: {self.result_median}', 
                             fontsize=14, fontweight='bold', color='green')
                ax2.set_ylabel('Valor', fontsize=12)
                ax2.set_xlabel(f'Comparações: {self.comparisons_median} | Partições: {self.partitions_median}', 
                              fontsize=11)
            
            # Adicionar legenda
            legend_elements = [
                plt.Rectangle((0, 0), 1, 1, fc='blue', label='Alvo (k-ésimo)'),
                plt.Rectangle((0, 0), 1, 1, fc='red', label='Pivô'),
                plt.Rectangle((0, 0), 1, 1, fc='yellow', label='Região Ativa'),
                plt.Rectangle((0, 0), 1, 1, fc='green', label='Encontrado'),
            ]
            fig.legend(handles=legend_elements, loc='lower center', ncol=4, 
                      bbox_to_anchor=(0.5, -0.02))
            
            plt.tight_layout()
        
        anim = animation.FuncAnimation(fig, update, frames=max_steps, 
                                      interval=interval, repeat=True)
        plt.show()
        return anim


class QuickSortVisualizer:
    def __init__(self, data, pivot_strategy_normal=None, pivot_name="Normal"):
        self.original_data = data.copy()
        self.data_normal = data.copy()
        self.data_median = data.copy()
        self.pivot_strategy_normal = pivot_strategy_normal or PivotStrategy.last_element
        self.pivot_name = pivot_name
        self.steps_normal = []
        self.steps_median = []
        self.comparisons_normal = 0
        self.comparisons_median = 0
        self.swaps_normal = 0
        self.swaps_median = 0
    
    def run_sorts(self):
        stats_normal = {'comparisons': 0, 'swaps': 0}
        if len(self.data_normal) > 0:
            quicksort(
                self.data_normal, 0, len(self.data_normal) - 1, 
                self.steps_normal, self.pivot_strategy_normal, stats_normal
            )
        self.comparisons_normal = stats_normal['comparisons']
        self.swaps_normal = stats_normal['swaps']
        
        stats_median = {'comparisons': 0, 'swaps': 0}
        if len(self.data_median) > 0:
            quicksort(
                self.data_median, 0, len(self.data_median) - 1, 
                self.steps_median, PivotStrategy.median_of_medians, stats_median
            )
        self.comparisons_median = stats_median['comparisons']
        self.swaps_median = stats_median['swaps']
    
    def animate(self, interval=100):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle(f'Comparação: QuickSort ({self.pivot_name}) vs QuickSort com Mediana das Medianas', 
                     fontsize=16, fontweight='bold')
        
        max_steps = max(len(self.steps_normal), len(self.steps_median))
        
        def update(frame):
            ax1.clear()
            ax2.clear()
            
            # QuickSort Normal
            if frame < len(self.steps_normal):
                step = self.steps_normal[frame]
                arr = step['array']
                left = step['left']
                right = step['right']
                pivot_idx = step['pivot_idx']
                
                colors = ['lightblue'] * len(arr)
                for i in range(left, right + 1):
                    colors[i] = 'yellow'
                if pivot_idx < len(colors):
                    colors[pivot_idx] = 'red'
                
                bars1 = ax1.bar(range(len(arr)), arr, color=colors, edgecolor='black')
                ax1.set_title(f'QuickSort ({self.pivot_name})\nPasso {frame + 1}/{len(self.steps_normal)}', 
                             fontsize=14, fontweight='bold')
                ax1.set_ylabel('Valor', fontsize=12)
                ax1.set_xlabel(f'Comparações: {self.comparisons_normal} | Trocas: {self.swaps_normal}', 
                              fontsize=11)
            else:
                arr = self.data_normal
                bars1 = ax1.bar(range(len(arr)), arr, color='green', edgecolor='black')
                ax1.set_title(f'QuickSort ({self.pivot_name}) - COMPLETO ✓', fontsize=14, 
                             fontweight='bold', color='green')
                ax1.set_ylabel('Valor', fontsize=12)
                ax1.set_xlabel(f'Comparações: {self.comparisons_normal} | Trocas: {self.swaps_normal}', 
                              fontsize=11)
            
            # QuickSort com Mediana das Medianas
            if frame < len(self.steps_median):
                step = self.steps_median[frame]
                arr = step['array']
                left = step['left']
                right = step['right']
                pivot_idx = step['pivot_idx']
                
                colors = ['lightcoral'] * len(arr)
                for i in range(left, right + 1):
                    colors[i] = 'lightyellow'
                if pivot_idx < len(colors):
                    colors[pivot_idx] = 'darkred'
                
                bars2 = ax2.bar(range(len(arr)), arr, color=colors, edgecolor='black')
                ax2.set_title(f'QuickSort com Mediana das Medianas\nPasso {frame + 1}/{len(self.steps_median)}', 
                             fontsize=14, fontweight='bold')
                ax2.set_ylabel('Valor', fontsize=12)
                ax2.set_xlabel(f'Comparações: {self.comparisons_median} | Trocas: {self.swaps_median}', 
                              fontsize=11)
            else:
                arr = self.data_median
                bars2 = ax2.bar(range(len(arr)), arr, color='darkgreen', edgecolor='black')
                ax2.set_title('QuickSort com Mediana das Medianas - COMPLETO ✓', 
                             fontsize=14, fontweight='bold', color='green')
                ax2.set_ylabel('Valor', fontsize=12)
                ax2.set_xlabel(f'Comparações: {self.comparisons_median} | Trocas: {self.swaps_median}', 
                              fontsize=11)
            
            # Adicionar legenda
            legend_elements = [
                plt.Rectangle((0, 0), 1, 1, fc='red', label='Pivô (Normal)'),
                plt.Rectangle((0, 0), 1, 1, fc='darkred', label='Pivô (Mediana)'),
                plt.Rectangle((0, 0), 1, 1, fc='yellow', label='Partição Ativa'),
            ]
            fig.legend(handles=legend_elements, loc='lower center', ncol=3, 
                      bbox_to_anchor=(0.5, -0.02))
            
            plt.tight_layout()
        
        anim = animation.FuncAnimation(fig, update, frames=max_steps, 
                                      interval=interval, repeat=True)
        plt.show()
        return anim


def select_pivot_strategy():
    print("\n" + "=" * 70)
    print("SELEÇÃO DE ESTRATÉGIA DE PIVÔ")
    print("=" * 70)
    print("\nEscolha a estratégia de pivô para a versão 'Normal':")
    print("1 - Último elemento (padrão)")
    print("2 - Primeiro elemento")
    print("3 - Elemento do meio")
    print("4 - Mediana de três elementos")
    print("5 - Elemento aleatório")
    
    pivot_choice = input("\nDigite o número da estratégia (1-5): ").strip()
    
    strategies = {
        "1": ("Último Elemento", PivotStrategy.last_element),
        "2": ("Primeiro Elemento", PivotStrategy.first_element),
        "3": ("Elemento do Meio", PivotStrategy.middle_element),
        "4": ("Mediana de Três", PivotStrategy.median_of_three),
        "5": ("Aleatório", PivotStrategy.random_element),
    }
    
    name, strategy = strategies.get(pivot_choice, ("Último Elemento", PivotStrategy.last_element))
    print(f"\nEstratégia selecionada: {name}")
    return name, strategy


def main():
    print("=" * 70)
    print("COMPARAÇÃO DE ALGORITMOS: Normal vs Mediana das Medianas")
    print("=" * 70)
    print("\nEscolha o algoritmo para comparar:")
    print("1 - QuickSort (ordenação completa)")
    print("2 - QuickSelect (encontrar k-ésimo elemento)")
    
    choice = input("\nDigite 1 ou 2: ").strip()
    
    pivot_name, pivot_strategy = select_pivot_strategy()
    
    if choice == "2":
        print("\n" + "=" * 70)
        print("QUICKSELECT - Encontrar k-ésimo menor elemento")
        print("=" * 70)
        
        print("\nGerando vetor ORDENADO (pior caso para QuickSelect Normal)...")
        n = 30
        data = np.arange(1, n + 1)
        
        print(f"Array original (ORDENADO): {data}")
        print(f"Tamanho: {len(data)} elementos")
        
        k = 0
        print(f"Buscando o {k+1}º menor elemento (índice {k})")
        print(f"Este é o PIOR CASO para QuickSelect com pivô no final!\n")
        
        visualizer = QuickSelectVisualizer(data, k, pivot_strategy, pivot_name)
        
        print(f"Executando QuickSelect com {pivot_name}...")
        print("Executando QuickSelect com Mediana das Medianas...")
        visualizer.run_selects()
        
        print(f"\nResultados:")
        print(f"QuickSelect com {pivot_name}:")
        print(f"  - Resultado encontrado: {visualizer.result_normal}")
        print(f"  - Comparações: {visualizer.comparisons_normal}")
        print(f"  - Partições realizadas: {visualizer.partitions_normal}")
        print(f"  - Passos na animação: {len(visualizer.steps_normal)}")
        
        print(f"\nQuickSelect com Mediana das Medianas:")
        print(f"  - Resultado encontrado: {visualizer.result_median}")
        print(f"  - Comparações: {visualizer.comparisons_median}")
        print(f"  - Partições realizadas: {visualizer.partitions_median}")
        print(f"  - Passos na animação: {len(visualizer.steps_median)}")
        
        print("\nIniciando animação...")
        visualizer.animate(interval=300)
        
    else:
        print("\n" + "=" * 70)
        print("QUICKSORT - Ordenação Completa")
        print("=" * 70)
        
        print("\nGerando vetor ORDENADO (pior caso para QuickSort Normal)...")
        n = 30
        data = np.arange(1, n + 1)
        
        print(f"Array original (ORDENADO): {data}")
        print(f"Tamanho: {len(data)} elementos")
        print(f"Este é o PIOR CASO para QuickSort com pivô no final!\n")
        
        visualizer = QuickSortVisualizer(data, pivot_strategy, pivot_name)
        
        print(f"Executando QuickSort com {pivot_name}...")
        print("Executando QuickSort com Mediana das Medianas...")
        visualizer.run_sorts()
        
        print(f"\nResultados:")
        print(f"QuickSort com {pivot_name}:")
        print(f"  - Comparações: {visualizer.comparisons_normal}")
        print(f"  - Trocas: {visualizer.swaps_normal}")
        print(f"  - Passos na animação: {len(visualizer.steps_normal)}")
        
        print(f"\nQuickSort com Mediana das Medianas:")
        print(f"  - Comparações: {visualizer.comparisons_median}")
        print(f"  - Trocas: {visualizer.swaps_median}")
        print(f"  - Passos na animação: {len(visualizer.steps_median)}")
        
        print(f"\nArray ordenado ({pivot_name}): {visualizer.data_normal}")
        print(f"Array ordenado (Mediana): {visualizer.data_median}")
        
        print("\nIniciando animação...")
        visualizer.animate(interval=200)


if __name__ == "__main__":
    main()