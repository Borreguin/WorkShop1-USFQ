def hanoi(num_disks, num_towers):
    if num_disks <= 0 or num_towers <= 0:
        print("Error: Number of disks and towers must be positive integers.")
        return

    # Define function to move disks recursively
    def move_disks(num_disks, source, target, auxiliary):
        if num_disks == 1:
            print(f"Move disk 1 from tower {source} to tower {target}")
            return
        move_disks(num_disks - 1, source, auxiliary, target)
        print(f"Move disk {num_disks} from tower {source} to tower {target}")
        move_disks(num_disks - 1, auxiliary, target, source)

    move_disks(num_disks, 1, num_towers, 2)


# Example usage:
num_disks = 3
num_towers = 3

hanoi(num_disks, num_towers)