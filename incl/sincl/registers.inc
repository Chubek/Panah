#define SYSC_NRR %rax
#define SYSC_RET %rax
#define SYSC_AG0 %rdi
#define SYSC_AG1 %rsi
#define SYSC_AG2 %rdx
#define SYSC_AG3 %r10
#define SYSC_AG4 %r8
#define SYSC_AG5 %r9

#define CABI_AG0 %rdi
#define CABI_AG1 %rsi
#define CABI_AG2 %rdx
#define CABI_AG3 %rcx
#define CABI_AG4 %r8
#define CABI_AG5 %r9
#define CABI_RET %rax

#define CNTR_QWD %rcx
#define CNTR_DWD %ecx
#define CNTR_WRD %cx
#define CNTR_LOB %cl
#define CNTR_HIB %ch

#define ACCM_QWD %rax
#define ACCM_DWD %eax
#define ACCM_WRD %ax
#define ACCM_LOB %al
#define ACCM_HIB %ah

#define STPT_QWD %rsp
#define STPT_DWD %esp
#define STPT_WRD %sp
#define STPT_LOW %spl

#define FPPT_QWD %rbp
#define FPPT_DWD %ebp
#define FPPT_WRD %bp
#define FPPT_LOW %bpl

#define CLB1_QWD %r10
#define CLB1_DWD %r10d
#define CLB1_WRD %r10w
#define CLB1_LOW %r10b

#define CLB2_QWD %r11
#define CLB2_DWD %r11d
#define CLB2_WRD %r11w
#define CLB2_LOW %r11b

#define CSV1_QWD %r8
#define CSV1_DWD %r8d
#define CSV1_WRD %r8w
#define CSV1_LOW %r8b

#define CSV2_QWD %r9
#define CSV2_DWD %r9d
#define CSV2_WRD %r9w
#define CSV2_LOW %r9b

#define CSV3_QWD %r12
#define CSV3_DWD %r12d
#define CSV3_WRD %r12w
#define CSV3_LOW %r12b

#define CSV4_QWD %r13
#define CSV4_DWD %r13d
#define CSV4_WRD %r13w
#define CSV4_LOW %r13b

#define CSV5_QWD %r14
#define CSV5_DWD %r14d
#define CSV5_WRD %r14w
#define CSV5_LOW %r14b

#define CSV6_QWD %r15
#define CSV6_DWD %r15d
#define CSV6_WRD %r15w
#define CSV6_LOW %r15b

#define SRCR_QWD %rsi
#define SRCR_DWD %esi
#define SRCR_WRD %si
#define SRCR_LOW %sil

#define DATA_QWD %rdx
#define DATA_DWD %edx
#define DATA_WRD %dx
#define DATA_LOB %dl
#define DATA_HIB %dh

#define DEST_QWD %rdi
#define DEST_DWD %edi
#define DEST_WRD %di
#define DEST_LOB %dl
#define DEST_HIB %dh

#define BASE_QWD %rbx
#define BASE_DWD %ebx
#define BASE_WRD %bx
#define BASE_LOB %bl
#define BASE_HIB %bh

#define OFST_QWD 8
#define OFST_DWD 4
#define OFST_WRD 2
#define OFST_LOW 1