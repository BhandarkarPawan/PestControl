import { Either, isLeft } from 'fp-ts/lib/Either';
import * as t from 'io-ts';

export interface IGraphQLClient {
  addUser(name: string, email: string, password: string): IMutationResponse;
  getUser(email: string): IUserResponse;
  addProject(title: string, description?: string): IMutationResponse;
  getProject(email: string): IProjectResponse;
  addIssue(
    project_id: string,
    title: string,
    description?: string,
    assigned_to?: string,
    due_date?: number,
    severity?: string,
    flag?: string,
    tags?: string[],
    classification?: string,
    reproducible?: string
  ): IMutationResponse;
  getIssue(email: string): IIssueResponse;
}

const MOptionalString = t.union([t.null, t.string]);
const MOptionalNumber = t.union([t.null, t.number]);
const MStringArray = t.array(t.string);

export const MMutationResponse = t.type({
  success: t.boolean,
  errors: MStringArray,
});

const MQueryResponseBase = t.type({
  success: t.boolean,
  errors: MStringArray,
});

export const MUser = t.type({
  id: t.number,
  name: t.string,
  email: t.string,
});

export const MUserResponse = t.intersection([
  MQueryResponseBase,
  t.type({
    info: t.union([MUser, t.null]),
  }),
]);

export const MProject = t.type({
  id: t.number,
  title: t.string,
  description: MOptionalString,
});

export const MProjectResponse = t.intersection([
  MQueryResponseBase,
  t.type({
    info: t.union([MProject, t.null]),
  }),
]);

export const MIssue = t.type({
  id: t.number,
  project_id: t.number,
  title: t.string,
  description: MOptionalString,
  assigned_to: MOptionalString,
  reported_date: t.number,
  due_date: MOptionalNumber,
  severity: MOptionalString,
  flag: MOptionalString,
  tags: MStringArray,
  classification: MOptionalString,
  reproducible: MOptionalString,
  project: MProject,
  assigned_user: MUser,
});

//Typescript
const add_two_numbers = (a: number, b: number) => {
  return a + b;
};

export const MIssueResponse = t.intersection([
  MQueryResponseBase,
  t.type({
    info: t.union([MIssue, t.null]),
  }),
]);

export type IMutationResponse = t.TypeOf<typeof MMutationResponse>;
export type IUserResponse = t.TypeOf<typeof MUserResponse>;
export type IProjectResponse = t.TypeOf<typeof MProjectResponse>;
export type IIssueResponse = t.TypeOf<typeof MIssueResponse>;
export type IUser = t.TypeOf<typeof MUser>;

export interface IGetUserVars {
  email: string;
}

export function checkDecodedObject<T>(
  decodedObject: Either<t.Errors, T>
): T | null {
  if (isLeft(decodedObject)) {
    // TODO: Log Error
    console.warn(`The received data did not pass the check`);
    return null;
  }
  return decodedObject.right as T;
}
