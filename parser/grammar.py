"""
grammar.py - the CONTEXT FREE GRAMMAR of the paper (pp. 117-130), copied
production by production.  Line k of GRAMMAR_TEXT is production k.

Format:  <lhs> -> symbol symbol ...      (λ = empty production)
A name written <like_this> is a non-terminal; anything else is a terminal,
spelled exactly like the lexer's token names (id, int_lit, Vary, +=, ...).
"""

GRAMMAR_TEXT = r"""
<program> -> <global_decl> <functions> <statements>
<global_decl> -> <global_item> <global_decl>
<global_decl> -> λ
<global_item> -> <var_decl> ;
<global_item> -> <const_decl> ;
<global_item> -> Recipe id <recipe_tail>
<recipe_tail> -> { <member> <member_tail> }
<recipe_tail> -> : id ;
<member_tail> -> <member> <member_tail>
<member_tail> -> λ
<member> -> id : <type_spec> ;
<var_decl> -> Vary id : <data_type> <var_tail>
<var_tail> -> = <base_init>
<var_tail> -> [ ] <arr_tail>
<arr_tail> -> = <array_1d_value>
<arr_tail> -> [ ] = <array_2d_value>
<base_init> -> <expression>
<base_init> -> Absorb ( )
<array_1d_value> -> <basket_1d>
<array_1d_value> -> <array_source>
<array_2d_value> -> <basket_2d>
<array_2d_value> -> <array_source>
<array_source> -> id <name_tail>
<basket_1d> -> Basket [ <elem_list> ]
<elem_list> -> <expression> <elem_tail>
<elem_list> -> λ
<elem_tail> -> , <expression> <elem_tail>
<elem_tail> -> λ
<basket_2d> -> Basket [ <row_items> ]
<row_items> -> <row_item> <row_items_tail>
<row_items> -> λ
<row_items_tail> -> , <row_item> <row_items_tail>
<row_items_tail> -> λ
<row_item> -> [ <elem_list> ]
<row_item> -> id <accessor>
<const_decl> -> Same id : <data_type> <const_tail>
<const_tail> -> = <base_init>
<const_tail> -> [ ] <const_arr>
<const_arr> -> = <same_basket_1d>
<const_arr> -> [ ] = <same_basket_2d>
<same_basket_1d> -> Basket [ <literal> <lit_tail> ]
<lit_tail> -> , <literal> <lit_tail>
<lit_tail> -> λ
<same_basket_2d> -> Basket [ <lit_row> <lit_row_tail> ]
<lit_row> -> [ <literal> <lit_tail> ]
<lit_row_tail> -> , <lit_row> <lit_row_tail>
<lit_row_tail> -> λ
<literal> -> int_lit
<literal> -> flo_lit
<literal> -> str_lit
<literal> -> boo_lit
<type_spec> -> <data_type> <dims>
<data_type> -> Number
<data_type> -> Rational
<data_type> -> Word
<data_type> -> Truth
<dims> -> [ ] <second_dims>
<dims> -> λ
<second_dims> -> [ ]
<second_dims> -> λ
<init_value> -> <expression>
<init_value> -> <basket_value>
<init_value> -> Absorb ( )
<basket_value> -> Basket [ <basket_body> ]
<basket_body> -> <basket_items>
<basket_body> -> λ
<basket_items> -> [ <elem_list> ] <row_items_tail>
<basket_items> -> <elem_not_name> <elem_tail>
<basket_items> -> id <basket_name_tail>
<basket_name_tail> -> ( <arguments> ) <expr_result_tail> <elem_tail>
<basket_name_tail> -> <accessor> <basket_after_name>
<basket_after_name> -> , <basket_items>
<basket_after_name> -> <expr_var_ops> <elem_tail>
<basket_after_name> -> λ
<elem_not_name> -> <num_literal_exp> <num_compare_tail>
<elem_not_name> -> <word_literal_exp> <word_compare_tail>
<elem_not_name> -> <truth_literal_exp> <truth_compare_tail>
<elem_not_name> -> ( <expression> ) <expr_result_tail>
<functions> -> <func_def> <functions>
<functions> -> λ
<func_def> -> Blend id ( <param_list> ) -> <return_type> <body>
<param_list> -> <param> <param_tail>
<param_list> -> λ
<param_tail> -> , <param> <param_tail>
<param_tail> -> λ
<param> -> id : <type_spec>
<return_type> -> Bland
<return_type> -> <type_spec>
<body> -> { <local_decls> <statements> }
<local_decls> -> <local_decl> <local_decls>
<local_decls> -> λ
<local_decl> -> <var_decl> ;
<local_decl> -> <const_decl> ;
<local_decl> -> Recipe id : id ;
<statements> -> <statement> <statements>
<statements> -> λ
<statement> -> id <id_stmt_tail> ;
<statement> -> <incdec_op> id <accessor> ;
<statement> -> Test <condition> <body> <stir_list> <taste_opt>
<statement> -> Harvest <harvest_value> { <try_clause> <try_list> Unripe <body> }
<statement> -> Mix <condition> <body>
<statement> -> Pour <body> Mix <condition> ;
<statement> -> Factor ( <factor_init> ; <factor_cond> ; <factor_step> ) <body>
<statement> -> Reap ;
<statement> -> Uproot ;
<statement> -> Produce <produce_value> ;
<statement> -> Squeeze ( <expression> ) ;
<statement> -> Append ( <array_target> , <arg> ) ;
<statement> -> Insert ( <array_target> , <index_exp> , <arg> ) ;
<statement> -> Remove ( <array_target> , <index_exp> ) ;
<statement> -> Clear ( <array_target> ) ;
<id_stmt_tail> -> ( <arguments> )
<id_stmt_tail> -> <accessor> <assign_tail>
<assign_tail> -> = <init_value>
<assign_tail> -> += <non_truth_exp>
<assign_tail> -> <num_assign_op> <num_exp>
<assign_tail> -> <incdec_op>
<non_truth_exp> -> <num_literal_exp>
<non_truth_exp> -> <word_literal_exp>
<non_truth_exp> -> <untyped_exp>
<num_assign_op> -> -=
<num_assign_op> -> *=
<num_assign_op> -> /=
<num_assign_op> -> %=
<incdec_op> -> ++
<incdec_op> -> --
<accessor> -> [ <index_exp> ] <second_index>
<accessor> -> . id <member_index>
<accessor> -> λ
<member_index> -> [ <index_exp> ] <second_index>
<member_index> -> λ
<second_index> -> [ <index_exp> ]
<second_index> -> λ
<index_exp> -> <int_exp>
<array_target> -> id <accessor>
<stir_list> -> Stir <condition> <body> <stir_list>
<stir_list> -> λ
<taste_opt> -> Taste <body>
<taste_opt> -> λ
<try_clause> -> Try <try_value> <body>
<try_list> -> <try_clause> <try_list>
<try_list> -> λ
<try_value> -> int_lit
<try_value> -> str_lit
<try_value> -> id
<factor_init> -> Vary id : <data_type> = <expression>
<factor_init> -> id <accessor> <factor_assign>
<factor_init> -> λ
<factor_cond> -> <condition>
<factor_cond> -> λ
<factor_step> -> id <accessor> <step_tail>
<factor_step> -> <incdec_op> id <accessor>
<factor_step> -> λ
<step_tail> -> <factor_assign>
<step_tail> -> <incdec_op>
<factor_assign> -> = <expression>
<factor_assign> -> += <non_truth_exp>
<factor_assign> -> <num_assign_op> <num_exp>
<produce_value> -> <expression>
<produce_value> -> λ
<arguments> -> <arg> <arg_tail>
<arguments> -> λ
<arg_tail> -> , <arg> <arg_tail>
<arg_tail> -> λ
<arg> -> <expression>
<arg> -> <basket_value>
<expression> -> <num_literal_exp> <num_compare_tail>
<expression> -> <word_literal_exp> <word_compare_tail>
<expression> -> <truth_literal_exp> <truth_compare_tail>
<expression> -> id <expr_name_tail>
<expression> -> ( <expression> ) <expr_result_tail>
<expr_name_tail> -> ( <arguments> ) <expr_result_tail>
<expr_name_tail> -> <accessor> <expr_var_tail>
<num_compare_tail> -> <compare_op> <num_exp> <logic_tail>
<num_compare_tail> -> λ
<word_compare_tail> -> <equal_op> <word_exp> <logic_tail>
<word_compare_tail> -> λ
<truth_compare_tail> -> <equal_op> <truth_unary> <logic_tail>
<truth_compare_tail> -> <logic_tail>
<expr_var_tail> -> <expr_var_ops>
<expr_var_tail> -> λ
<expr_var_ops> -> <incdec_op> <pow_tail> <mul_tail> <add_tail> <num_compare_tail>
<expr_var_ops> -> <expr_result_ops>
<expr_result_tail> -> <expr_result_ops>
<expr_result_tail> -> λ
<expr_result_ops> -> ^ <num_unary> <mul_tail> <add_tail> <num_compare_tail>
<expr_result_ops> -> <mul_op> <num_unary> <mul_tail> <add_tail> <num_compare_tail>
<expr_result_ops> -> - <num_term> <add_tail> <num_compare_tail>
<expr_result_ops> -> + <expr_after_plus>
<expr_result_ops> -> <rel_op> <num_exp> <logic_tail>
<expr_result_ops> -> <equal_op> <any_exp> <logic_tail>
<expr_result_ops> -> And <logic_operand> <and_tail> <or_tail>
<expr_result_ops> -> Or <logic_operand> <and_tail> <or_tail>
<expr_after_plus> -> <num_literal_start> <mul_tail> <add_tail> <num_compare_tail>
<expr_after_plus> -> <word_value> <word_tail> <word_compare_tail>
<expr_after_plus> -> id <expr_plus_name_tail>
<expr_after_plus> -> ( <expression> ) <expr_plus_result_tail>
<expr_plus_name_tail> -> ( <arguments> ) <expr_plus_result_tail>
<expr_plus_name_tail> -> <accessor> <expr_plus_var_tail>
<expr_plus_var_tail> -> <incdec_op> <pow_tail> <mul_tail> <add_tail> <num_compare_tail>
<expr_plus_var_tail> -> <expr_plus_result_tail>
<expr_plus_result_tail> -> ^ <num_unary> <mul_tail> <add_tail> <num_compare_tail>
<expr_plus_result_tail> -> <mul_op> <num_unary> <mul_tail> <add_tail> <num_compare_tail>
<expr_plus_result_tail> -> - <num_term> <add_tail> <num_compare_tail>
<expr_plus_result_tail> -> + <expr_after_plus>
<expr_plus_result_tail> -> <rel_op> <num_exp> <logic_tail>
<expr_plus_result_tail> -> <equal_op> <non_truth_exp> <logic_tail>
<expr_plus_result_tail> -> λ
<logic_tail> -> <and_tail> <or_tail>
<condition> -> <logic_operand> <logic_tail>
<and_tail> -> And <logic_operand> <and_tail>
<and_tail> -> λ
<or_tail> -> Or <logic_operand> <and_tail> <or_tail>
<or_tail> -> λ
<logic_operand> -> <num_literal_exp> <compare_op> <num_exp>
<logic_operand> -> <word_literal_exp> <equal_op> <word_exp>
<logic_operand> -> <truth_literal_exp> <cond_truth_compare>
<logic_operand> -> id <cond_name_tail>
<logic_operand> -> ( <expression> ) <cond_result_tail>
<cond_truth_compare> -> <equal_op> <truth_unary>
<cond_truth_compare> -> λ
<cond_name_tail> -> ( <arguments> ) <cond_result_tail>
<cond_name_tail> -> <accessor> <cond_var_tail>
<cond_var_tail> -> <incdec_op> <pow_tail> <mul_tail> <add_tail> <compare_op> <num_exp>
<cond_var_tail> -> <cond_result_tail>
<cond_result_tail> -> ^ <num_unary> <mul_tail> <add_tail> <compare_op> <num_exp>
<cond_result_tail> -> <mul_op> <num_unary> <mul_tail> <add_tail> <compare_op> <num_exp>
<cond_result_tail> -> - <num_term> <add_tail> <compare_op> <num_exp>
<cond_result_tail> -> + <cond_after_plus>
<cond_result_tail> -> <rel_op> <num_exp>
<cond_result_tail> -> <equal_op> <any_exp>
<cond_result_tail> -> λ
<cond_after_plus> -> <num_literal_start> <mul_tail> <add_tail> <compare_op> <num_exp>
<cond_after_plus> -> <word_value> <word_tail> <equal_op> <word_exp>
<cond_after_plus> -> id <cond_plus_name_tail>
<cond_after_plus> -> ( <expression> ) <cond_plus_result_tail>
<cond_plus_name_tail> -> ( <arguments> ) <cond_plus_result_tail>
<cond_plus_name_tail> -> <accessor> <cond_plus_var_tail>
<cond_plus_var_tail> -> <incdec_op> <pow_tail> <mul_tail> <add_tail> <compare_op> <num_exp>
<cond_plus_var_tail> -> <cond_plus_result_tail>
<cond_plus_result_tail> -> ^ <num_unary> <mul_tail> <add_tail> <compare_op> <num_exp>
<cond_plus_result_tail> -> <mul_op> <num_unary> <mul_tail> <add_tail> <compare_op> <num_exp>
<cond_plus_result_tail> -> - <num_term> <add_tail> <compare_op> <num_exp>
<cond_plus_result_tail> -> + <cond_after_plus>
<cond_plus_result_tail> -> <rel_op> <num_exp>
<cond_plus_result_tail> -> <equal_op> <non_truth_exp>
<any_exp> -> <num_literal_exp>
<any_exp> -> <word_literal_exp>
<any_exp> -> <truth_literal_exp>
<any_exp> -> <untyped_exp>
<num_literal_exp> -> <num_literal_start> <mul_tail> <add_tail>
<num_literal_start> -> ~ <num_unary>
<num_literal_start> -> <num_value> <pow_tail>
<num_literal_start> -> <incdec_value> <pow_tail>
<num_exp> -> <num_term> <add_tail>
<add_tail> -> + <num_term> <add_tail>
<add_tail> -> - <num_term> <add_tail>
<add_tail> -> λ
<num_term> -> <num_unary> <mul_tail>
<mul_tail> -> <mul_op> <num_unary> <mul_tail>
<mul_tail> -> λ
<num_unary> -> ~ <num_unary>
<num_unary> -> <num_operand> <pow_tail>
<pow_tail> -> ^ <num_unary>
<pow_tail> -> λ
<num_operand> -> <num_value>
<num_operand> -> <incdec_value>
<num_operand> -> <untyped_num_operand>
<num_value> -> int_lit
<num_value> -> flo_lit
<num_value> -> ToNumber ( <expression> )
<num_value> -> ToRational ( <expression> )
<num_value> -> Length ( <length_arg> )
<incdec_value> -> <incdec_op> id <accessor>
<length_arg> -> <word_literal_exp>
<length_arg> -> <untyped_operand> <word_tail>
<harvest_value> -> <int_literal_exp>
<harvest_value> -> <word_literal_exp>
<harvest_value> -> id <harvest_name_tail>
<harvest_value> -> ( <expression> ) <harvest_result_tail>
<harvest_name_tail> -> ( <arguments> ) <harvest_result_tail>
<harvest_name_tail> -> <accessor> <harvest_var_tail>
<harvest_var_tail> -> <incdec_op> <int_pow_tail> <int_mul_tail> <int_add_tail>
<harvest_var_tail> -> <harvest_result_tail>
<harvest_result_tail> -> ^ <int_unary> <int_mul_tail> <int_add_tail>
<harvest_result_tail> -> <int_mul_op> <int_unary> <int_mul_tail> <int_add_tail>
<harvest_result_tail> -> - <int_term> <int_add_tail>
<harvest_result_tail> -> + <harvest_value>
<harvest_result_tail> -> λ
<int_literal_exp> -> <int_literal_start> <int_mul_tail> <int_add_tail>
<int_literal_start> -> ~ <int_unary>
<int_literal_start> -> <int_value> <int_pow_tail>
<int_literal_start> -> <incdec_value> <int_pow_tail>
<int_exp> -> <int_term> <int_add_tail>
<int_add_tail> -> + <int_term> <int_add_tail>
<int_add_tail> -> - <int_term> <int_add_tail>
<int_add_tail> -> λ
<int_term> -> <int_unary> <int_mul_tail>
<int_mul_tail> -> <int_mul_op> <int_unary> <int_mul_tail>
<int_mul_tail> -> λ
<int_unary> -> ~ <int_unary>
<int_unary> -> <int_operand> <int_pow_tail>
<int_pow_tail> -> ^ <int_unary>
<int_pow_tail> -> λ
<int_operand> -> <int_value>
<int_operand> -> <incdec_value>
<int_operand> -> <untyped_num_operand>
<int_value> -> int_lit
<int_value> -> ToNumber ( <expression> )
<int_value> -> Length ( <length_arg> )
<word_literal_exp> -> <word_value> <word_tail>
<word_exp> -> <word_operand> <word_tail>
<word_tail> -> + <word_operand> <word_tail>
<word_tail> -> λ
<word_operand> -> <word_value>
<word_operand> -> <untyped_operand>
<word_value> -> str_lit
<word_value> -> ToWord ( <expression> )
<truth_literal_exp> -> <truth_value>
<truth_literal_exp> -> Not <truth_unary>
<truth_unary> -> Not <truth_unary>
<truth_unary> -> <truth_value>
<truth_unary> -> <untyped_operand>
<truth_value> -> boo_lit
<truth_value> -> ToTruth ( <expression> )
<untyped_exp> -> id <untyped_name_tail>
<untyped_exp> -> ( <expression> ) <untyped_result_tail>
<untyped_name_tail> -> ( <arguments> ) <untyped_result_tail>
<untyped_name_tail> -> <accessor> <untyped_var_tail>
<untyped_var_tail> -> <incdec_op> <pow_tail> <mul_tail> <add_tail>
<untyped_var_tail> -> <untyped_result_tail>
<untyped_result_tail> -> ^ <num_unary> <mul_tail> <add_tail>
<untyped_result_tail> -> <mul_op> <num_unary> <mul_tail> <add_tail>
<untyped_result_tail> -> - <num_term> <add_tail>
<untyped_result_tail> -> + <non_truth_exp>
<untyped_result_tail> -> λ
<untyped_operand> -> id <name_tail>
<untyped_operand> -> ( <expression> )
<name_tail> -> ( <arguments> )
<name_tail> -> <accessor>
<untyped_num_operand> -> id <untyped_num_tail>
<untyped_num_operand> -> ( <expression> )
<untyped_num_tail> -> ( <arguments> )
<untyped_num_tail> -> <accessor> <postfix>
<postfix> -> <incdec_op>
<postfix> -> λ
<compare_op> -> <rel_op>
<compare_op> -> <equal_op>
<rel_op> -> >
<rel_op> -> <
<rel_op> -> >=
<rel_op> -> <=
<equal_op> -> ==
<equal_op> -> !=
<mul_op> -> *
<mul_op> -> /
<mul_op> -> %
<int_mul_op> -> *
<int_mul_op> -> %
"""

START = "<program>"
END = "$"
EPSILON = "λ"


def _parse(text):
    prods = []
    for line in text.strip().splitlines():
        lhs, rhs = line.split("->", 1)
        syms = rhs.split()
        if syms == [EPSILON]:
            syms = []
        prods.append((lhs.strip(), syms))
    return prods


# PRODUCTIONS[k - 1] is production k of the paper: (lhs, [rhs symbols])
PRODUCTIONS = _parse(GRAMMAR_TEXT)


def is_nonterminal(sym):
    return sym.startswith("<") and sym.endswith(">") and len(sym) > 2
