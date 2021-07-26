import { Either, isLeft } from 'fp-ts/lib/Either';
import * as t from 'io-ts';

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
  id: t.string,
  name: t.string,
  email: t.string,
});

export const MUserResponse = t.intersection([
  MQueryResponseBase,
  t.type({
    info: t.union([MUser, t.null]),
  }),
]);

export const MUsersResponse = t.intersection([
  MQueryResponseBase,
  t.type({
    info: t.array(MUser),
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

export const MIssueResponse = t.intersection([
  MQueryResponseBase,
  t.type({
    info: t.union([MIssue, t.null]),
  }),
]);

export const MGetUserResponse = t.type({
  getUsers: MUsersResponse,
});

export type IMutationResponse = t.TypeOf<typeof MMutationResponse>;
export type IUser = t.TypeOf<typeof MUser>;
export type IUserResponse = t.TypeOf<typeof MUserResponse>;
export type IUsersResponse = t.TypeOf<typeof MUsersResponse>;
export type IGetUserResponse = t.TypeOf<typeof MGetUserResponse>;
export type IProjectResponse = t.TypeOf<typeof MProjectResponse>;
export type IIssueResponse = t.TypeOf<typeof MIssueResponse>;

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
