import salmon.lang as sal
from salmon.comp import dagonly
from salmon.codegen import spark, CodeGenConfig
from salmon.utils import *

@dagonly
def simple_div():

    colsInA = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("c", "INTEGER", [1])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    div1 = sal.divide(in1, "div1", "a", ["a", "b"])

    opened = sal.collect(div1, 1)

    # return root nodes
    return set([in1])


@dagonly
def comp_div():

    colsInA = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("c", "INTEGER", [1])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    # divide column 0 by columns 1 & 2, then divide by 5 (scalar)
    div1 = sal.divide(in1, "div1", "a", ["a", "b", "c", 5])

    opened = sal.collect(div1, 1)

    # return root nodes
    return set([in1])


@dagonly
def simple_mult():
    colsInA = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("c", "INTEGER", [1])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    mult1 = sal.multiply(in1, "mult1", "a", ["a", "b"])

    opened = sal.collect(mult1, 1)

    # return root nodes
    return set([in1])


@dagonly
def comp_mult():
    colsInA = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("c", "INTEGER", [1])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    # multiply column 0 by columns 1 & 2, then multiply by 5 (scalar)
    mult1 = sal.multiply(in1, "mult1", "a", ["a", "b", "c", 5])

    opened = sal.collect(mult1, 1)

    # return root nodes
    return set([in1])


@dagonly
def create_col_mult():
    colsInA = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("c", "INTEGER", [1])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    mult1 = sal.multiply(in1, "mult1", "d", ["a", "b"])

    opened = sal.collect(mult1, 1)

    return set([in1])


@dagonly
def create_col_div():
    colsInA = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("c", "INTEGER", [1])
    ]
    in1 = sal.create("in1", colsInA, set([1]))

    div1 = sal.divide(in1, "div1", "d", ["a", "b"])

    opened = sal.collect(div1, 1)

    return set([in1])


@dagonly
def multicol_agg():
    colsInA = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("c", "INTEGER", [1])
    ]
    in1 = sal.create('in1', colsInA, set([1]))

    agg1 = sal.aggregate(in1, 'agg1', ['a', 'b'], 'c', '+', 'c')

    opened = sal.collect(agg1, 1)

    return set([in1])


@dagonly
def multicol_join():
    colsInA = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("c", "INTEGER", [1])
    ]

    colsInB = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("d", "INTEGER", [1])
    ]

    in1 = sal.create('in1', colsInA, set([1]))
    in2 = sal.create('in2', colsInB, set([1]))

    join1 = sal.join(in1, in2, 'join1', ['a', 'b'], ['a', 'b'])

    opened = sal.collect(join1, 1)

    return set([in1])


@dagonly
def index():

    colsInA = [
        defCol("a", "INTEGER", [1]),
        defCol("b", "INTEGER", [1]),
        defCol("c", "INTEGER", [1])
    ]

    in1 = sal.create('in1', colsInA, set([1]))

    index = sal.index(in1, "index")

    opened = sal.collect(index, 1)

    return set([in1])

if __name__ == "__main__":

    config = CodeGenConfig()

    simple_mult_dag = simple_mult()
    simple_mult = spark.SparkCodeGen(config, simple_mult_dag)
    job = simple_mult.generate("simple_mult", "/tmp")

    comp_mult_dag = comp_mult()
    comp_mult = spark.SparkCodeGen(config, comp_mult_dag)
    job = comp_mult.generate("comp_mult", "/tmp")

    simple_div_dag = simple_div()
    simple_div = spark.SparkCodeGen(config, simple_div_dag)
    job = simple_div.generate("simple_div", "/tmp")

    comp_div_dag = comp_div()
    comp_div = spark.SparkCodeGen(config, comp_div_dag)
    job = comp_div.generate("comp_div", "/tmp")

    create_mult_dag = create_col_mult()
    create_mult = spark.SparkCodeGen(config, create_mult_dag)
    job = create_mult.generate("create_mult", "/tmp")

    create_div_dag = create_col_div()
    create_div = spark.SparkCodeGen(config, create_div_dag)
    job = create_div.generate("create_div", "/tmp")

    multicol_agg_dag = multicol_agg()
    multicol_agg = spark.SparkCodeGen(config, multicol_agg_dag)
    job = multicol_agg.generate('multicol_agg', '/tmp')

    multicol_join_dag = multicol_join()
    multicol_join = spark.SparkCodeGen(config, multicol_join_dag)
    job = multicol_join.generate('multicol_join', '/tmp')

    index_dag = index()
    index = spark.SparkCodeGen(config, index_dag)
    job = index.generate('index', '/tmp')

    print("Spark code generated in {}".format(config.code_path))