class Status {
    static Passed = 'Passed';
    static Failed = 'Failed';
    static Error = 'Error';
}

class Result {
    constructor(status, message) {
        this.status = status;
        this.message = message;
    }

    static error(error) {
        return new Result(Status.Error, `Error:\n${error}`);
    }

    static failed(expected, got) {
        return new Result(Status.Failed, `Fail: expected=${expected} got=${got}`);
    }

    static passed() {
        return new Result(Status.Passed, 'OK!');
    }
}


async function run(code, input) {
    console.log(`Gona run ${code} with ${input}`)
    let pyodide = await loadPyodide()
    pyodide.setStdin(new StdinHandler([input]))
    let out = new StdoutHandler()
    pyodide.setStdout({ batched: (msg) => out.add(msg) })
    await pyodide.runPython(code)
    return out.build()
}

async function test(code, input, expected) {
    try {
        let got = await run(code, input)
        if (got === expected)
            return Result.passed()
        else
            return Result.failed(expected, got)
    } catch (error) {
        return Result.error(error)
    }
}

class StdinHandler {
    constructor(lines) {
        this.lines = lines;
        this.idx = 0;
    }

    stdin() {
        return this.lines[this.idx++];
    }
}


class StdoutHandler {
    constructor() {
        this.lines = [];
    }

    add(string) {
        this.lines.push(string)
    }

    build() {
        return this.lines.join('\n');
    }
}