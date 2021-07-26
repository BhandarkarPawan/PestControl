import { DocumentNode, useQuery } from '@apollo/client';
import { Either, isLeft } from 'fp-ts/lib/Either';
import * as t from 'io-ts';

export function checkDecodedObject<T>(
  decodedObject: Either<t.Errors, T>
): T | null {
  if (isLeft(decodedObject)) {
    console.warn(`The received data did not pass the check`);
    return null;
  }
  return decodedObject.right as T;
}

export function useGraphQL<T, V>(
  query: DocumentNode,
  typeC: t.Type<T>,
  vars?: V
) {
  const { loading, data } = useQuery<T>(query, { variables: vars });
  console.log('Data:', data);
  /* debugger */
  if (!loading) {
    const response = checkDecodedObject(typeC.decode(data));
    return { loading, response };
  } else {
    return { loading, response: null };
  }
}

export default useGraphQL;
