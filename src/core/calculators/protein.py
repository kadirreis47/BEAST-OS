GOALS={
"fat_loss":2.0,
"maintenance":1.6,
"muscle_gain":2.2
}
def protein_target(weight,goal):
    return round(weight*GOALS[goal])
