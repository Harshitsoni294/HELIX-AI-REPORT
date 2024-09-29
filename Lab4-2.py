import random
from music21 import stream, note, midi

asc = ['C', 'C#', 'E', 'F', 'G', 'G#', 'B']
desc = ['C', 'B', 'G#', 'G', 'F', 'E', 'C#']

def generate(length):
    return [random.choice(asc if random.random() > 0.5 else desc) for _ in range(length)]

def cost(melody):
    fitness = 0
    for pattern in [asc, desc]:
        for i in range(len(melody) - len(pattern) + 1):
            if melody[i:i + len(pattern)] == pattern:
                fitness += 10
                fitness += sum(j for j in range(2, len(pattern)) if melody[i:i + j] == pattern[:j])
    return fitness

def transition(parent1, parent2):
    split = random.randint(1, len(parent1) - 1)
    return parent1[:split] + parent2[split:], parent2[:split] + parent1[split:]

def change(melody, mutation_rate=0.1):
    return [random.choice(asc if random.random() > 0.5 else desc) if random.random() < mutation_rate else note for note in melody]

def genetic_algorithm(generations=1000, population_size=100, mutation_rate=0.1, melody_length=64):
    population = [generate(melody_length) for _ in range(population_size)]
    best_melody = []

    for generation in range(generations):
        fitness_scores = [(melody, cost(melody)) for melody in population]
        best_melody = max(fitness_scores, key=lambda x: x[1])[0]
        print(f"Generation {generation}: Best Melody: {' '.join(best_melody)} with Fitness: {cost(best_melody)}")

        selected = [melody for melody, score in sorted(fitness_scores, key=lambda x: x[1], reverse=True)[:population_size // 2]]
        population = [change(child) for parent1, parent2 in (transition(random.choice(selected), random.choice(selected)) for _ in range(population_size)) for child in [parent1, parent2]]

    return best_melody

def melody_to_stream(melody):
    return stream.Stream([note.Note(swara) for swara in melody])

best_melody = genetic_algorithm()
s = melody_to_stream(best_melody)

mf = midi.translate.music21ObjectToMidiFile(s)
mf.open("raag_bhairav_melody_corrected.mid", 'wb')
mf.write()
mf.close()
