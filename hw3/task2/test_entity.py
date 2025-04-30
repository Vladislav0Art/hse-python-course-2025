import numpy as np
import os
from entity import Entity

def main():
    np.random.seed(0)

    entity_a = Entity(np.random.randint(0, 10, (5, 5)))
    entity_b = Entity(np.random.randint(0, 10, (5, 5)))

    print("Entity A:")
    print(entity_a)
    print()
    print("Entity B:")
    print(entity_b)
    print()

    addition = entity_a + entity_b
    subtraction = entity_a - entity_b
    multiplication = entity_a * entity_b
    # +1 to avoid div by zero
    division = entity_a / (entity_b + 1)

    # property access: set/get
    entity_a.name = "Entity A"
    entity_b.name = "Entity B"

    print(f"Entity A name: {entity_a.name}")
    print(f"Entity B name: {entity_b.name}")

    # saving into artifacts dir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(os.path.dirname(script_dir), "artifacts", "task2")
    os.makedirs(artifacts_dir, exist_ok=True)

    # some props to entities
    addition.operation = "addition"
    addition.description = "sum of Entity A and Entity B"

    subtraction.operation = "subtraction"
    subtraction.description = "diff between Entity A and Entity B"

    multiplication.operation = "multiplication"
    multiplication.description = "element-wise product of Entity A and Entity B"

    division.operation = "division"
    division.description = "element-wise division of Entity A by (Entity B + 1)"

    # save in files via mixin's method
    addition.save_to_file(os.path.join(artifacts_dir, "entity_plus.txt"))
    subtraction.save_to_file(os.path.join(artifacts_dir, "entity_minus.txt"))
    multiplication.save_to_file(os.path.join(artifacts_dir, "entity_mult.txt"))
    division.save_to_file(os.path.join(artifacts_dir, "entity_div.txt"))

    print()
    print("==== Success: operations completed and results saved to text files ====")

if __name__ == "__main__":
    main()
