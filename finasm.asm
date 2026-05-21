.data
    welcome:     .asciiz "\n--- FinASM: MIPS Expense Tracker ---\n"
    menu:        .asciiz "1. Add Income\n2. Add Expense\n3. View Summary Table\n4. Exit\nChoice: "
    inc_cat_menu: .asciiz "\nIncome Category:\n1. Salary\n2. Business\n3. Rental Income\n4. Government Benefits\n5. Commissions\n6. Other Income\nChoice: "
    exp_cat_menu: .asciiz "\nExpense Category:\n1. Food\n2. Savings & Investments\n3. Transport\n4. Medical\n5. Home Insurance\n6. Personal & Family\n7. Entertainment\n8. Other\nChoice: "
    inc_msg:     .asciiz "Enter income amount: "
    exp_msg:     .asciiz "Enter expense amount: "
    
    table_hdr:   .asciiz "\nType | Category           | Amount\n-----------------------------------\n"
    mes:         .asciiz "\nGenerating Summary...\n" 
    newline:     .asciiz "\n"
    inc_lbl:     .asciiz " [I] | "
    exp_lbl:     .asciiz " [E] | "
    
    # Income Category Names
    ic1: .asciiz "Salary            | Rs"
    ic2: .asciiz "Business          | Rs"
    ic3: .asciiz "Rental Income     | Rs"
    ic4: .asciiz "Govt Benefits     | Rs"
    ic5: .asciiz "Commissions       | Rs"
    ic6: .asciiz "Other Income      | Rs"
    
    # Expense Category Names
    ec1: .asciiz "Food              | Rs"
    ec2: .asciiz "Savings           | Rs"
    ec3: .asciiz "Transport         | Rs"
    ec4: .asciiz "Medical           | Rs"
    ec5: .asciiz "Home Insurance    | Rs"
    ec6: .asciiz "Personal & Family | Rs"
    ec7: .asciiz "Entertainment     | Rs"
    ec8: .asciiz "Other Expense     | Rs"
    total_lbl: .asciiz "Total Balance       | Rs"
    
    # Storage (Max 50)
    
    history_amt: .word 0:50     
    history_typ: .byte 0:50     
    history_cat: .word 0:50     

.text
.globl main
main:
    li $s0, 0          # Total Balance
    li $s1, 0          # Counter

menu_loop:
    li $v0, 4
    la $a0, welcome
    syscall
    la $a0, menu
    syscall

    li $v0, 5
    syscall
    move $t0, $v0      

    beq $t0, 1, add_income
    beq $t0, 2, add_expense
    beq $t0, 3, show_table
    beq $t0, 4, exit_program
    j menu_loop

add_income:
    li $v0, 4
    la $a0, inc_msg
    syscall
    li $v0, 5
    syscall
    move $t1, $v0      
    add $s0, $s0, $t1  

    li $v0, 4
    la $a0, inc_cat_menu
    syscall
    li $v0, 5
    syscall
    move $t8, $v0       
    
    li $t2, 'I'        
    jal store_data
    j menu_loop

add_expense:
    li $v0, 4
    la $a0, exp_msg
    syscall
    li $v0, 5
    syscall
    move $t1, $v0      
    sub $s0, $s0, $t1  

    li $v0, 4
    la $a0, exp_cat_menu
    syscall
    li $v0, 5
    syscall
    move $t8, $v0       
    
    li $t2, 'E'        
    jal store_data
    j menu_loop

store_data:
    li $t3, 50
    beq $s1, $t3, full
    sll $t4, $s1, 2    
    sw $t1, history_amt($t4)
    sw $t8, history_cat($t4)
    sb $t2, history_typ($s1)
    addi $s1, $s1, 1
full:
    jr $ra

show_table:
    li $v0, 4
    la $a0, mes
    syscall
    la $a0, table_hdr
    syscall
    li $t5, 0          

table_loop:
    beq $t5, $s1, total
    
    lb $t6, history_typ($t5)
    sll $t7, $t5, 2
    lw $t9, history_cat($t7)   

    li $v0, 4
    beq $t6, 'I', print_inc_row
    
    # Print Expense Row
    la $a0, exp_lbl
    syscall
    beq $t9, 1, e1
    beq $t9, 2, e2
    beq $t9, 3, e3
    beq $t9, 4, e4
    beq $t9, 5, e5
    beq $t9, 6, e6
    beq $t9, 7, e7
    la $a0, ec8       # Default to Other Expense
    j print_val
    
    e1: la $a0, ec1
        j print_val
    e2: la $a0, ec2
        j print_val
    e3: la $a0, ec3
        j print_val
    e4: la $a0, ec4
        j print_val
    e5: la $a0, ec5
        j print_val
    e6: la $a0, ec6
        j print_val
    e7: la $a0, ec7
        j print_val

print_inc_row:
    la $a0, inc_lbl
    syscall
    beq $t9, 1, i1
    beq $t9, 2, i2
    beq $t9, 3, i3
    beq $t9, 4, i4
    beq $t9, 5, i5
    la $a0, ic6       # Default to Other Income
    j print_val
    
    i1: la $a0, ic1
        j print_val
    i2: la $a0, ic2
        j print_val
    i3: la $a0, ic3
        j print_val
    i4: la $a0, ic4
        j print_val
    i5: la $a0, ic5
        j print_val

print_val:
    syscall            
    lw $a0, history_amt($t7)
    li $v0, 1          
    syscall
    
    li $v0, 4
    la $a0, newline
    syscall
    addi $t5, $t5, 1
    j table_loop
 
total:
li $v0, 4
    la $a0, total_lbl
    syscall
    
    move $a0, $s0      # Move net balance to $a0
    li $v0, 1          # Print balance
    syscall
    
    li $v0, 4
    la $a0, newline
    syscall
    syscall            # Double space for neatness
    j menu_loop

exit_program:
    li $v0, 10
    syscall