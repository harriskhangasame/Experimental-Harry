import React, { forwardRef } from "react";
import SvgLangChainIcon from "./LangChainIcon";

export const LangChainIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  return <SvgLangChainIcon ref={ref} {...props} />;
});
