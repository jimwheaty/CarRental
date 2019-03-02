export interface User {
    username: string,
    password: string
}
export class User {
    constructor(
        public username: string,
        public password: string
    ){}
}
